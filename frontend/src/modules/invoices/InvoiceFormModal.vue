<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { projectsApi, projectKeys } from "@/modules/projects/api"
import { FormModal } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Select } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { Textarea } from "@/shared/components/ui/textarea"

import { invoiceKeys, invoicesApi } from "./api"
import type { Invoice, InvoiceWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Invoice | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; saved: [] }>()
const { t } = useI18n()
const queryClient = useQueryClient()

// Load projects for the selector
const { data: projectsData } = useQuery({
  queryKey: projectKeys.list({ page_size: 100 }),
  queryFn: () => projectsApi.list({ page_size: 100 }),
})

const projectOptions = computed(() =>
  (projectsData.value?.items ?? []).map((p) => ({
    value: p.id,
    label: p.name,
  })),
)

interface FormState {
  project_id: string | null
  amount: string
  tax: string
  issue_date: string
  due_date: string
  notes: string
}

const today = () => new Date().toISOString().slice(0, 10)
const in30Days = () =>
  new Date(Date.now() + 30 * 86400000).toISOString().slice(0, 10)

const empty = (): FormState => ({
  project_id: null,
  amount: "0",
  tax: "0",
  issue_date: today(),
  due_date: in30Days(),
  notes: "",
})

const form = ref<FormState>(empty())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    if (c) {
      form.value = {
        project_id: null,
        amount: c.amount,
        tax: c.tax,
        issue_date: c.issue_date,
        due_date: c.due_date,
        notes: c.notes,
      }
    } else {
      form.value = empty()
    }
  },
  { immediate: true },
)

const { mutate: save, isPending } = useMutation({
  mutationFn: () => {
    if (props.editing) {
      // Only amount/tax/dates/notes can change on update — project stays
      const { project_id, ...rest } = form.value
      return invoicesApi.update(props.editing.id, rest)
    }
    return invoicesApi.create({
      project_id: form.value.project_id!,
      amount: form.value.amount,
      tax: form.value.tax || "0",
      issue_date: form.value.issue_date,
      due_date: form.value.due_date,
      notes: form.value.notes,
    } satisfies InvoiceWritePayload)
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: invoiceKeys.all })
    emit("saved")
  },
  onError: (err) => {
    if (err instanceof ApiError) {
      fieldErrors.value = err.fieldErrors()
      generalError.value = err.firstError()
    } else {
      generalError.value = t("common.error")
    }
  },
})

function submit() {
  generalError.value = ""
  fieldErrors.value = {}

  if (!props.editing && !form.value.project_id) {
    fieldErrors.value.project_id = [t("invoices.form.project_required")]
    return
  }
  if (!form.value.amount || Number(form.value.amount) < 0) {
    fieldErrors.value.amount = [t("invoices.form.amount_required")]
    return
  }
  if (form.value.issue_date && form.value.due_date && form.value.due_date < form.value.issue_date) {
    fieldErrors.value.due_date = [t("invoices.form.due_after_issue")]
    return
  }
  save()
}

const err = (k: string) => fieldErrors.value[k]?.[0] ?? null

const total = computed(
  () => Number(form.value.amount || 0) + Number(form.value.tax || 0),
)
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('invoices.edit_title') : $t('invoices.new')"
    max-width="lg"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <!-- Project (only on create) -->
      <div v-if="!props.editing">
        <label class="text-sm font-medium">{{ $t("invoices.form.project") }} *</label>
        <Select
          v-model="form.project_id"
          :options="projectOptions"
          :placeholder="$t('invoices.form.select_project')"
        />
        <p v-if="err('project_id')" class="text-xs text-rose-600">{{ err("project_id") }}</p>
      </div>

      <!-- Amount + tax -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("invoices.form.amount") }} *</label>
          <Input
            v-model="form.amount"
            type="number"
            min="0"
            step="0.01"
            :class="err('amount') && 'border-rose-500'"
          />
          <p v-if="err('amount')" class="text-xs text-rose-600">{{ err("amount") }}</p>
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("invoices.form.tax") }}</label>
          <Input v-model="form.tax" type="number" min="0" step="0.01" />
          <p v-if="err('tax')" class="text-xs text-rose-600">{{ err("tax") }}</p>
        </div>
      </div>

      <!-- Total preview -->
      <div class="flex items-center justify-between rounded-md bg-slate-50 px-3 py-2 text-sm dark:bg-slate-800">
        <span class="text-slate-600 dark:text-slate-400">{{ $t("invoices.form.total") }}</span>
        <span class="font-semibold tabular-nums">{{ total.toLocaleString() }}</span>
      </div>

      <!-- Dates -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("invoices.form.issue") }}</label>
          <Input
            v-model="form.issue_date"
            type="date"
            :class="err('issue_date') && 'border-rose-500'"
          />
          <p v-if="err('issue_date')" class="text-xs text-rose-600">{{ err("issue_date") }}</p>
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("invoices.form.due") }}</label>
          <Input
            v-model="form.due_date"
            type="date"
            :class="err('due_date') && 'border-rose-500'"
          />
          <p v-if="err('due_date')" class="text-xs text-rose-600">{{ err("due_date") }}</p>
        </div>
      </div>

      <!-- Notes -->
      <div>
        <label class="text-sm font-medium">{{ $t("invoices.form.notes") }}</label>
        <Textarea v-model="form.notes" :rows="2" />
      </div>

      <p
        v-if="generalError"
        class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
      >
        {{ generalError }}
      </p>
    </div>

    <template #actions>
      <Button variant="outline" @click="emit('close')">{{ $t("common.cancel") }}</Button>
      <Button :disabled="isPending" @click="submit">
        <Spinner v-if="isPending" size="sm" />
        <span v-else>{{ $t("common.save") }}</span>
      </Button>
    </template>
  </FormModal>
</template>