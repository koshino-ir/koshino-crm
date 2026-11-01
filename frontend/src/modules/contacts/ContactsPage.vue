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

import { contactKeys, contactsApi } from "./api"
import ContactFormModal from "./ContactFormModal.vue"
import type { Contact } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const debouncedSearch = useDebouncedRef(search, 300)
watch(debouncedSearch, () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    contactKeys.list({ page: page.value, search: debouncedSearch.value }),
  ),
  queryFn: () =>
    contactsApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const showForm = ref(false)
const editing = ref<Contact | null>(null)
const deleting = ref<Contact | null>(null)

const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => contactsApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: contactKeys.all })
    deleting.value = null
  },
})

const columns = computed(() => [
  { key: "full_name", label: t("contacts.columns.name") },
  { key: "company", label: t("contacts.columns.company") },
  { key: "email", label: t("contacts.columns.email") },
  { key: "phone", label: t("contacts.columns.phone") },
  { key: "is_primary", label: t("contacts.columns.primary"), align: "center" as const },
  { key: "actions", label: "", align: "end" as const },
])
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-4">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.contacts") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("contacts.subtitle") }}</p>
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
          {{ $t("contacts.new") }}
        </Button>
      </div>

      <Input
        v-model="search"
        :placeholder="$t('contacts.search_placeholder')"
        class="max-w-sm"
      />

      <DataTable
        :columns="columns"
        :rows="rows"
        :loading="isLoading"
        :empty-message="$t('contacts.empty')"
      >
        <template #cell:company="{ row }">
          <span v-if="row.company">{{ row.company.name }}</span>
          <span v-else class="text-slate-400">—</span>
        </template>
        <template #cell:is_primary="{ row }">
          <span
            v-if="row.is_primary"
            class="inline-block rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
          >✓</span>
          <span v-else class="text-slate-300">—</span>
        </template>
        <template #cell:actions="{ row }">
          <div class="flex justify-end gap-1">
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

    <ContactFormModal
      :open="showForm"
      :editing="editing"
      @close="showForm = false"
      @saved="showForm = false"
    />

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('contacts.delete_confirm', { name: deleting?.full_name ?? '' })"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>