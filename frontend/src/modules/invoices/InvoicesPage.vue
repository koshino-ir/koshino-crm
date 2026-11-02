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

import { invoiceKeys, invoicesApi } from "./api"
import InvoiceFormModal from "./InvoiceFormModal.vue"
import type { Invoice, InvoiceStatus } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const statusFilter = ref<string | null>(null)
const debouncedSearch = useDebouncedRef(search, 300)
watch([debouncedSearch, statusFilter], () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    invoiceKeys.list({
      page: page.value,
      search: debouncedSearch.value,
      status: statusFilter.value,
    }),
  ),
  queryFn: () =>
    invoicesApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
      status: statusFilter.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Invoice | null>(null)
const deleting = ref<Invoice | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => invoicesApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: invoiceKeys.all })
    deleting.value = null
  },
})

const { mutate: markPaid, isPending: isMarkingPaid } = useMutation({
  mutationFn: (inv: Invoice) => invoicesApi.markPaid(inv.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: invoiceKeys.all })
  },
})

const statusColors: Record<InvoiceStatus, string> = {
  draft: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
  sent: "bg-sky-100 text-sky-700 dark:bg-sky-950/40 dark:text-sky-300",
  paid: "bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300",
  overdue: "bg-rose-100 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300",
  cancelled: "bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-500 line-through",
}

const columns = computed(() => [
  { key: "number", label: t("invoices.columns.number") },
  { key: "total", label: t("invoices.columns.total"), align: "end" as const },
  { key: "status", label: t("invoices.columns.status"), align: "center" as const },
  { key: "issue_date", label: t("invoices.columns.issue") },
  { key: "due_date", label: t("invoices.columns.due") },
  { key: "actions", label: "", align: "end" as const },
])

const statusOptions = computed(() => [
  { value: "", label: t("invoices.filters.all") },
  { value: "draft", label: t("invoices.statuses.draft") },
  { value: "sent", label: t("invoices.statuses.sent") },
  { value: "paid", label: t("invoices.statuses.paid") },
  { value: "overdue", label: t("invoices.statuses.overdue") },
  { value: "cancelled", label: t("invoices.statuses.cancelled") },
])

function openCreate() {
  editing.value = null
  showForm.value = true
}

function openEdit(inv: Invoice) {
  editing.value = inv
  showForm.value = true
}

const canMarkPaid = (inv: Invoice) =>
  inv.status === "sent" || inv.status === "overdue"

const isOverdue = (inv: Invoice) =>
  inv.status !== "paid" &&
  inv.status !== "cancelled" &&
  inv.due_date < new Date().toISOString().slice(0, 10)
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.invoices") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("invoices.subtitle") }}</p>
        </div>
        <Button @click="openCreate">
          <Plus class="h-4 w-4" />
          {{ $t("invoices.new") }}
        </Button>
      </div>

      <div class="flex flex-wrap gap-2">
        <Input
          v-model="search"
          :placeholder="$t('invoices.search_placeholder')"
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
        :empty-message="$t('invoices.empty')"
      >
        <template #cell:number="{ row }">
          <span class="font-mono text-sm">{{ row.number }}</span>
        </template>
        <template #cell:total="{ row }">
          <span class="tabular-nums font-medium">
            {{ Number(row.total).toLocaleString() }}
          </span>
        </template>
        <template #cell:status="{ row }">
          <span
            class="inline-block rounded-full px-2 py-0.5 text-xs"
            :class="statusColors[row.status]"
          >
            {{ $t(`invoices.statuses.${row.status}`) }}
          </span>
        </template>
        <template #cell:due_date="{ row }">
          <span
            :class="isOverdue(row) ? 'text-rose-600 font-medium' : ''"
          >
            {{ row.due_date }}
          </span>
        </template>
        <template #cell:actions="{ row }">
          <div class="flex justify-end gap-1">
            <button
              v-if="canMarkPaid(row)"
              class="rounded p-1.5 text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/30 disabled:opacity-40"
              :title="$t('invoices.mark_paid')"
              :disabled="isMarkingPaid"
              @click="markPaid(row)"
            >
              <CheckCircle2 class="h-4 w-4" />
            </button>
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

    <InvoiceFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('invoices.delete_confirm', { name: deleting?.number ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>