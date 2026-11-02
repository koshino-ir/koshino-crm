<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { Phone, Mail, Users, FileText, Plus, Trash2 } from "lucide-vue-next"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { useDebouncedRef } from "@/core/utils/useDebouncedRef"
import { ConfirmDialog, Pagination } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { AppLayout } from "@/shared/layouts"

import { activityKeys, activitiesApi } from "./api"
import type { Activity } from "./types"

const { t } = useI18n()
const queryClient = useQueryClient()

const page = ref(1)
const search = ref("")
const typeFilter = ref<string | null>(null)
const debouncedSearch = useDebouncedRef(search, 300)
watch([debouncedSearch, typeFilter], () => (page.value = 1))

const { data, isLoading } = useQuery({
  queryKey: computed(() =>
    activityKeys.list({
      page: page.value,
      search: debouncedSearch.value,
      type: typeFilter.value,
    }),
  ),
  queryFn: () =>
    activitiesApi.list({
      page: page.value,
      search: debouncedSearch.value || undefined,
      type: typeFilter.value || undefined,
    }),
})

const rows = computed(() => data.value?.items ?? [])
const meta = computed(() => data.value?.meta)

const deleting = ref<Activity | null>(null)
const { mutate: doDelete, isPending: isDeleting } = useMutation({
  mutationFn: () => activitiesApi.delete(deleting.value!.id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: activityKeys.all })
    deleting.value = null
  },
})

const icons = { call: Phone, email: Mail, meeting: Users, note: FileText }

const typeOptions = computed(() => [
  { value: "", label: t("activities.filters.all") },
  { value: "call", label: t("activities.types.call") },
  { value: "email", label: t("activities.types.email") },
  { value: "meeting", label: t("activities.types.meeting") },
  { value: "note", label: t("activities.types.note") },
])
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-4xl space-y-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("nav.activities") }}
        </h1>
        <p class="text-sm text-slate-500">{{ $t("activities.subtitle") }}</p>
      </div>

      <div class="flex flex-wrap gap-2">
        <Input
          v-model="search"
          :placeholder="$t('activities.search_placeholder')"
          class="max-w-sm"
        />
        <select
          :value="typeFilter ?? ''"
          class="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          @change="typeFilter = (($event.target as HTMLSelectElement).value) || null"
        >
          <option v-for="o in typeOptions" :key="o.value" :value="o.value">
            {{ o.label }}
          </option>
        </select>
      </div>

      <div v-if="isLoading" class="flex justify-center py-8">
        <Spinner />
      </div>

      <Card v-else-if="rows.length === 0" class="p-8 text-center text-slate-500">
        {{ $t("activities.empty") }}
      </Card>

      <Card v-else class="p-4">
        <ul class="space-y-3">
          <li
            v-for="a in rows"
            :key="a.id"
            class="flex items-start gap-3 rounded-md border border-slate-100 p-3 dark:border-slate-800"
          >
            <div class="rounded-md bg-primary-50 p-2 text-primary-600 dark:bg-primary-950/40 dark:text-primary-400">
              <component :is="icons[a.type]" class="h-4 w-4" />
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2">
                <span class="font-medium text-slate-900 dark:text-slate-100">{{ a.subject }}</span>
                <span class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] uppercase text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                  {{ $t(`activities.types.${a.type}`) }}
                </span>
              </div>
              <p v-if="a.description" class="mt-1 text-sm text-slate-600 dark:text-slate-400">
                {{ a.description }}
              </p>
              <div class="mt-1 text-xs text-slate-500">
                {{ a.created_by?.first_name || a.created_by?.email }} ·
                {{ new Date(a.occurred_at).toLocaleString() }}
              </div>
            </div>
            <button
              class="rounded p-1 text-slate-400 hover:text-rose-500"
              @click="deleting = a"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </li>
        </ul>
      </Card>

      <Pagination
        v-if="meta"
        :page="meta.page"
        :total-pages="meta.total_pages"
        :total="meta.count"
        @change="(p) => (page = p)"
      />

      <div class="flex justify-center">
        <RouterLink :to="{ name: 'deals' }">
          <Button variant="outline">
            <Plus class="h-4 w-4" />
            {{ $t("activities.add_hint") }}
          </Button>
        </RouterLink>
      </div>
    </div>

    <ConfirmDialog
      :open="!!deleting"
      :title="$t('common.delete')"
      :message="$t('activities.delete_confirm')"
      :confirm-label="$t('common.delete')"
      :cancel-label="$t('common.cancel')"
      :loading="isDeleting"
      @cancel="deleting = null"
      @confirm="doDelete()"
    />
  </AppLayout>
</template>