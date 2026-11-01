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

import { companiesApi, companyKeys } from "./api"
import CompanyFormModal from "./CompanyFormModal.vue"
import type { Company } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const debouncedSearch = useDebouncedRef(search, 300)
watch(debouncedSearch, () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    companyKeys.list({ page: page.value, search: debouncedSearch.value }),
  ),
  queryFn: () =>
    companiesApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Company | null>(null)
const deleting = ref<Company | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => companiesApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: companyKeys.all })
    deleting.value = null
  },
})

function openCreate() {
  editing.value = null
  showForm.value = true
}
function openEdit(c: Company) {
  editing.value = c
  showForm.value = true
}

const columns = computed(() => [
  { key: "name", label: t("companies.columns.name") },
  { key: "industry", label: t("companies.columns.industry") },
  { key: "email", label: t("companies.columns.email") },
  { key: "phone", label: t("companies.columns.phone") },
  { key: "contacts_count", label: t("companies.columns.contacts"), align: "center" as const },
  { key: "actions", label: "", align: "end" as const },
])
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.companies") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("companies.subtitle") }}</p>
        </div>
        <Button @click="openCreate">
          <Plus class="h-4 w-4" />
          {{ $t("companies.new") }}
        </Button>
      </div>

      <Input
        v-model="search"
        :placeholder="$t('companies.search_placeholder')"
        class="max-w-sm"
      />

      <DataTable
        :columns="columns"
        :rows="rows"
        :loading="isLoading"
        :empty-message="$t('companies.empty')"
      >
        <template #cell:industry="{ row }">
          <span class="text-slate-600 dark:text-slate-400">{{ row.industry || "—" }}</span>
        </template>
        <template #cell:email="{ row }">
          <a
            v-if="row.email"
            :href="`mailto:${row.email}`"
            class="text-primary-600 hover:underline"
          >{{ row.email }}</a>
          <span v-else class="text-slate-400">—</span>
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

    <CompanyFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('companies.delete_confirm', { name: deleting?.name ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>