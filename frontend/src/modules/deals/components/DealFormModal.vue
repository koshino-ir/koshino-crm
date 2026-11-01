<script setup lang="ts">
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { ref } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"

import { dealsApi } from "../api"
import { dealKeys } from "../api/keys"
import type { Pipeline } from "../types"
import CompanySelect from "./CompanySelect.vue"

interface Props {
  pipeline: Pipeline | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; created: [] }>()

const { t } = useI18n()
const queryClient = useQueryClient()

const form = ref({
  title: "",
  company_id: null as string | null,
  amount: "0",
  currency: "IRR",
  expected_close_date: "",
  probability: "50",
})

const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

const { mutate: submitDeal, isPending } = useMutation({
  mutationFn: () =>
    dealsApi.create({
      title: form.value.title.trim(),
      company_id: form.value.company_id!,
      pipeline_id: props.pipeline!.id,
      amount: form.value.amount || "0",
      currency: form.value.currency,
      expected_close_date: form.value.expected_close_date || null,
      probability: Number(form.value.probability) || 0,
    }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: dealKeys.all })
    emit("created")
  },
  onError: (err) => {
    if (err instanceof ApiError) {
      fieldErrors.value = err.fieldErrors()
      generalError.value = err.firstError()
    } else {
      generalError.value = err instanceof Error ? err.message : t("common.error")
    }
  },
})

function submit() {
  generalError.value = ""
  fieldErrors.value = {}
  if (!form.value.title.trim()) {
    fieldErrors.value.title = [t("deals.form.title_required")]
    return
  }
  if (!form.value.company_id) {
    fieldErrors.value.company_id = [t("deals.form.company_required")]
    return
  }
  if (!props.pipeline) {
    generalError.value = t("deals.form.no_pipeline")
    return
  }
  submitDeal()
}

function fieldError(name: string): string | null {
  const list = fieldErrors.value[name]
  return list && list.length > 0 ? list[0] : null
}
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    @click.self="emit('close')"
  >
    <div class="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl dark:bg-slate-900">
      <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100">
        {{ $t("deals.new") }}
      </h2>

      <div class="mt-4 space-y-3">
        <div>
          <label class="text-sm font-medium">{{ $t("deals.form.title") }}</label>
          <Input v-model="form.title" :class="fieldError('title') && 'border-rose-500'" />
          <p v-if="fieldError('title')" class="text-xs text-rose-600">
            {{ fieldError("title") }}
          </p>
        </div>

        <div>
          <label class="text-sm font-medium">{{ $t("deals.form.company") }}</label>
          <CompanySelect v-model="form.company_id" />
          <p v-if="fieldError('company_id')" class="text-xs text-rose-600">
            {{ fieldError("company_id") }}
          </p>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-sm font-medium">{{ $t("deals.form.amount") }}</label>
            <Input v-model="form.amount" type="number" min="0" />
            <p v-if="fieldError('amount')" class="text-xs text-rose-600">
              {{ fieldError("amount") }}
            </p>
          </div>
          <div>
            <label class="text-sm font-medium">{{ $t("deals.form.currency") }}</label>
            <select
              v-model="form.currency"
              class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
            >
              <option>IRR</option>
              <option>USD</option>
              <option>EUR</option>
              <option>AED</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-sm font-medium">{{ $t("deals.form.expected_close") }}</label>
            <Input v-model="form.expected_close_date" type="date" />
          </div>
          <div>
            <label class="text-sm font-medium">{{ $t("deals.form.probability") }}</label>
            <Input v-model="form.probability" type="number" min="0" max="100" />
          </div>
        </div>

        <p
          v-if="generalError"
          class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
        >
          {{ generalError }}
        </p>
      </div>

      <div class="mt-6 flex justify-end gap-2">
        <Button variant="outline" @click="emit('close')">
          {{ $t("deals.form.cancel") }}
        </Button>
        <Button :disabled="isPending" @click="submit">
          <Spinner v-if="isPending" size="sm" />
          <span v-else>{{ $t("deals.form.create") }}</span>
        </Button>
      </div>
    </div>
  </div>
</template>