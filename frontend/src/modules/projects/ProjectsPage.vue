<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { Pencil, Plus, Trash2 } from "lucide-vue-next"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { useDebouncedRef } from "@/core/utils/useDebouncedRef"
import { ConfirmDialog, DataTable, Pagination } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { AppLayout } from "@/shared/layouts"

import { projectKeys, projectsApi } from "./api"
import ProjectFormModal from "./ProjectFormModal.vue"
import type { Project, ProjectStatus } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const statusFilter = ref<string | null>(null)
const debouncedSearch = useDebouncedRef(search, 300)
watch([debouncedSearch, statusFilter], () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    projectKeys.list({
      page: page.value,
      search: debouncedSearch.value,
      status: statusFilter.value,
    }),
  ),
  queryFn: () =>
    projectsApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
      status: statusFilter.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Project | null>(null)
const deleting = ref<Project | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => projectsApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: projectKeys.all })
    deleting.value = null
  },
})

const statusColors: Record<ProjectStatus, string> = {
  planning: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
  active: "bg-sky-100 text-sky-700 dark:bg-sky-950/40 dark:text-sky-300",
  on_hold: "bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300",
  completed: "bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300",
  cancelled: "bg-rose-100 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300",
}

const columns = computed(() => [
  { key: "name", label: t("projects.columns.name") },
  { key: "client_company", label: t("projects.columns.client") },
  { key: "status", label: t("projects.columns.status"), align: "center" as const },
  { key: "budget", label: t("projects.columns.budget"), align: "end" as const },
  { key: "invoices_count", label: t("projects.columns.invoices"), align: "center" as const },
  { key: "actions", label: "", align: "end" as const },
])

const statusOptions = computed(() => [
  { value: "", label: t("projects.filters.all") },
  { value: "planning", label: t("projects.statuses.planning") },
  { value: "active", label: t("projects.statuses.active") },
  { value: "on_hold", label: t("projects.statuses.on_hold") },
  { value: "completed", label: t("projects.statuses.completed") },
  { value: "cancelled", label: t("projects.statuses.cancelled") },
])

function openCreate() {
  editing.value = null
  showForm.value = true
}

function openEdit(p: Project) {
  editing.value = p
  showForm.value = true
}
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.projects") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("projects.subtitle") }}</p>
        </div>
        <Button @click="openCreate">
          <Plus class="h-4 w-4" />
          {{ $t("projects.new") }}
        </Button>
      </div>

      <div class="flex flex-wrap gap-2">
        <Input
          v-model="search"
          :placeholder="$t('projects.search_placeholder')"
          class="max-w-sm"
        />
        <select
          :value="statusFilter ?? ''"
          class="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          @change="statusFilter = ($event.target as HTMLSelectElement).value || null"
        >
          <option v-for="o in statusOptions" :key="o.value" :value="o.value">
            {{ o.label }}
          </option>
        </select>
      </div>

      <DataTable
        :columns="columns"
        :rows="rows"
        :loading="isLoading"
        :empty-message="$t('projects.empty')"
      >
        <template #cell:client_company="{ row }">
          {{ row.client_company.name }}
        </template>
        <template #cell:status="{ row }">
          <span
            class="inline-block rounded-full px-2 py-0.5 text-xs"
            :class="statusColors[row.status]"
          >
            {{ $t(`projects.statuses.${row.status}`) }}
          </span>
        </template>
        <template #cell:budget="{ row }">
          <span class="tabular-nums">{{ Number(row.budget).toLocaleString() }}</span>
        </template>
        <template #cell:actions="{ row }">
          <div class="flex justify-end gap-1">
            <button
              class="rounded p-1.5 text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800"
              @click="openEdit(row)"
            >
              <Pencil class="h-4 w-4" />
            </button>
            <button
              class="rounded p-1.5 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30"
              @click="deleting = row"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </template>
      </DataTable>

      <Pagination
        v-if="meta"
        :page="meta.page"
        :total-pages="meta.total_pages"
        :total="meta.count"
        @change="(p) => (page = p)"
      />
    </div>

    <ProjectFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('projects.delete_confirm', { name: deleting?.name ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>