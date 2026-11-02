<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { CheckCircle2, Pencil, Plus, Trash2 } from "lucide-vue-next"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { useDebouncedRef } from "@/core/utils/useDebouncedRef"
import { ConfirmDialog, DataTable, Pagination } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { AppLayout } from "@/shared/layouts"

import { taskKeys, tasksApi } from "./api"
import TaskFormModal from "./TaskFormModal.vue"
import type { Task } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const statusFilter = ref<string | null>(null)
const debouncedSearch = useDebouncedRef(search, 300)
watch([debouncedSearch, statusFilter], () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    taskKeys.list({
      page: page.value,
      search: debouncedSearch.value,
      status: statusFilter.value,
    }),
  ),
  queryFn: () =>
    tasksApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
      status: statusFilter.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Task | null>(null)
const deleting = ref<Task | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => tasksApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: taskKeys.all })
    deleting.value = null
  },
})

const { mutate: toggleDone } = useMutation({
  mutationFn: (task: Task) =>
    task.status === "done" ? tasksApi.reopen(task.id) : tasksApi.complete(task.id),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: taskKeys.all }),
})

const priorityColors: Record<string, string> = {
  low: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
  medium: "bg-sky-100 text-sky-700 dark:bg-sky-950/40 dark:text-sky-300",
  high: "bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300",
  urgent: "bg-rose-100 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300",
}

const columns = computed(() => [
  { key: "done", label: "", align: "center" as const, thClass: "w-12" },
  { key: "title", label: t("tasks.columns.title") },
  { key: "priority", label: t("tasks.columns.priority"), align: "center" as const },
  { key: "due_date", label: t("tasks.columns.due") },
  { key: "status", label: t("tasks.columns.status") },
  { key: "actions", label: "", align: "end" as const },
])

const statusOptions = computed(() => [
  { value: "", label: t("tasks.filters.all") },
  { value: "todo", label: t("tasks.statuses.todo") },
  { value: "in_progress", label: t("tasks.statuses.in_progress") },
  { value: "done", label: t("tasks.statuses.done") },
])
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.tasks") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("tasks.subtitle") }}</p>
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
          {{ $t("tasks.new") }}
        </Button>
      </div>

      <div class="flex flex-wrap gap-2">
        <Input
          v-model="search"
          :placeholder="$t('tasks.search_placeholder')"
          class="max-w-sm"
        />
        <select
          :value="statusFilter ?? ''"
          class="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          @change="statusFilter = (($event.target as HTMLSelectElement).value) || null"
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
        :empty-message="$t('tasks.empty')"
      >
        <template #cell:done="{ row }">
          <button
            class="rounded-full p-0.5"
            :class="row.status === 'done' ? 'text-emerald-500' : 'text-slate-300 hover:text-slate-500'"
            @click="toggleDone(row)"
          >
            <CheckCircle2 class="h-5 w-5" />
          </button>
        </template>
        <template #cell:title="{ row }">
          <span :class="row.status === 'done' && 'line-through text-slate-400'">
            {{ row.title }}
          </span>
        </template>
        <template #cell:priority="{ row }">
          <span
            class="inline-block rounded-full px-2 py-0.5 text-xs"
            :class="priorityColors[row.priority]"
          >
            {{ $t(`tasks.priorities.${row.priority}`) }}
          </span>
        </template>
        <template #cell:due_date="{ row }">
          <span :class="row.due_date && new Date(row.due_date) < new Date() && row.status !== 'done' ? 'text-rose-600 font-medium' : ''">
            {{ row.due_date ?? "—" }}
          </span>
        </template>
        <template #cell:status="{ row }">
          {{ $t(`tasks.statuses.${row.status}`) }}
        </template>
        <template #cell:actions="{ row }">
          <div class="flex justify-end gap-1">
            <button
              class="rounded p-1.5 text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
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

    <TaskFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('tasks.delete_confirm', { name: deleting?.title ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>