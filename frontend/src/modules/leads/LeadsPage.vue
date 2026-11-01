<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { ArrowRight, Pencil, Plus, Trash2 } from "lucide-vue-next"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { useDebouncedRef } from "@/core/utils/useDebouncedRef"
import { ConfirmDialog, DataTable, Pagination } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { AppLayout } from "@/shared/layouts"

import { leadKeys, leadsApi } from "./api"
import ConvertLeadDialog from "./ConvertLeadDialog.vue"
import LeadFormModal from "./LeadFormModal.vue"
import type { Lead } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const debouncedSearch = useDebouncedRef(search, 300)
watch(debouncedSearch, () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    leadKeys.list({ page: page.value, search: debouncedSearch.value }),
  ),
  queryFn: () =>
    leadsApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Lead | null>(null)
const deleting = ref<Lead | null>(null)
const converting = ref<Lead | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => leadsApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: leadKeys.all })
    deleting.value = null
  },
})

const columns = computed(() => [
  { key: "title", label: t("leads.columns.title") },
  { key: "company", label: t("leads.columns.company") },
  { key: "source", label: t("leads.columns.source") },
  { key: "status", label: t("leads.columns.status") },
  { key: "actions", label: "", align: "end" as const },
])

const statusColors: Record<string, string> = {
  new: "bg-sky-100 text-sky-700 dark:bg-sky-950/40 dark:text-sky-300",
  contacted: "bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300",
  qualified: "bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300",
  unqualified: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
}
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.leads") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("leads.subtitle") }}</p>
        </div>
        <Button
          @click="
            () => {
              editing = null
              showForm = true
            }
          "
        >
          <Plus class="h-4 w-4" />
          {{ $t("leads.new") }}
        </Button>
      </div>

      <Input
        v-model="search"
        :placeholder="$t('leads.search_placeholder')"
        class="max-w-sm"
      />

      <DataTable
        :columns="columns"
        :rows="rows"
        :loading="isLoading"
        :empty-message="$t('leads.empty')"
      >
        <template #cell:company="{ row }">
          <span v-if="row.company">{{ row.company.name }}</span>
          <span v-else class="text-slate-400">—</span>
        </template>
        <template #cell:source="{ row }">
          {{ $t(`leads.sources.${row.source}`) }}
        </template>
        <template #cell:status="{ row }">
          <span
            class="inline-block rounded-full px-2 py-0.5 text-xs"
            :class="statusColors[row.status]"
          >
            {{ $t(`leads.statuses.${row.status}`) }}
          </span>
        </template>
        <template #cell:actions="{ row }">
          <div class="flex justify-end gap-1">
            <button
              v-if="row.status === 'qualified'"
              class="rounded p-1.5 text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/30"
              :title="$t('leads.convert.title')"
              @click="converting = row"
            >
              <ArrowRight class="h-4 w-4 rtl:rotate-180" />
            </button>
            <button
              class="rounded p-1.5 text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800"
              @click="
                () => {
                  editing = row
                  showForm = true
                }
              "
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

    <LeadFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConvertLeadDialog
      :open="!!converting"
      :lead="converting"
      @close="converting = null"
      @converted="converting = null"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('leads.delete_confirm', { name: deleting?.title ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>