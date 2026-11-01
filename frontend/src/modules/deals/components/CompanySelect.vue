<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { Plus } from "lucide-vue-next"
import { ref } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { Input } from "@/shared/components/ui/input"

import { companiesApi } from "../api"
import { companyKeys } from "../api/keys"

interface Props {
  modelValue: string | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ "update:modelValue": [id: string | null] }>()

const { t } = useI18n()
const queryClient = useQueryClient()
const showCreate = ref(false)
const newName = ref("")
const error = ref("")

const { data: companies } = useQuery({
  queryKey: companyKeys.all,
  queryFn: () => companiesApi.list(),
})

const { mutate: createCompany, isPending: isCreating } = useMutation({
  mutationFn: (name: string) => companiesApi.create({ name }),
  onSuccess: (company) => {
    queryClient.invalidateQueries({ queryKey: companyKeys.all })
    emit("update:modelValue", company.id)
    showCreate.value = false
    newName.value = ""
  },
  onError: (err) => {
    error.value =
      err instanceof ApiError ? err.firstError() : t("common.error")
  },
})

function submitCreate() {
  if (!newName.value.trim()) return
  error.value = ""
  createCompany(newName.value.trim())
}

function onSelect(e: Event) {
  const v = (e.target as HTMLSelectElement).value
  emit("update:modelValue", v || null)
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex gap-2">
      <select
        :value="props.modelValue ?? ''"
        class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
        @change="onSelect"
      >
        <option value="">{{ $t("deals.form.select_company") }}</option>
        <option v-for="c in companies ?? []" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
      <button
        type="button"
        class="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
        :title="$t('deals.form.company_name')"
        @click="showCreate = !showCreate"
      >
        <Plus class="h-4 w-4" />
      </button>
    </div>

    <div
      v-if="showCreate"
      class="space-y-2 rounded-md border border-slate-200 bg-slate-50 p-3 dark:border-slate-700 dark:bg-slate-800"
    >
      <Input
        v-model="newName"
        :placeholder="$t('deals.form.company_name')"
        @keydown.enter.prevent="submitCreate"
      />
      <p v-if="error" class="text-xs text-rose-600">{{ error }}</p>
      <div class="flex justify-end gap-2">
        <button
          type="button"
          class="text-sm text-slate-500 hover:text-slate-700"
          @click="showCreate = false"
        >
          {{ $t("deals.form.cancel") }}
        </button>
        <button
          type="button"
          class="text-sm font-medium text-primary-600 hover:underline disabled:opacity-50"
          :disabled="isCreating"
          @click="submitCreate"
        >
          {{ isCreating ? $t("deals.form.saving") : $t("deals.form.save") }}
        </button>
      </div>
    </div>
  </div>
</template>