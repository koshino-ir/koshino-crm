<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { companiesApi, companyKeys } from "@/modules/companies/api"
import { FormModal } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Select } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { Textarea } from "@/shared/components/ui/textarea"

import { leadKeys, leadsApi } from "./api"
import type { Lead, LeadSource, LeadStatus, LeadWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Lead | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; saved: [] }>()

const { t } = useI18n()
const queryClient = useQueryClient()

// --- Companies lookup ---

const { data: companiesData } = useQuery({
  queryKey: companyKeys.list({ page_size: 100 }),
  queryFn: () => companiesApi.list({ page_size: 100 }),
})

const companyOptions = computed(() =>
  (companiesData.value?.items ?? []).map((c) => ({
    value: c.id,
    label: c.name,
  })),
)

// --- Dropdown options from i18n ---

const sourceOptions = computed(() => [
  { value: "web", label: t("leads.sources.web") },
  { value: "referral", label: t("leads.sources.referral") },
  { value: "social", label: t("leads.sources.social") },
  { value: "event", label: t("leads.sources.event") },
  { value: "cold_call", label: t("leads.sources.cold_call") },
  { value: "other", label: t("leads.sources.other") },
])

const statusOptions = computed(() => [
  { value: "new", label: t("leads.statuses.new") },
  { value: "contacted", label: t("leads.statuses.contacted") },
  { value: "qualified", label: t("leads.statuses.qualified") },
  { value: "unqualified", label: t("leads.statuses.unqualified") },
])

// --- Form state ---

interface FormState extends Omit<LeadWritePayload, "company_id" | "contact_id"> {
  company_id: string | null
  contact_id: string | null
}

const emptyForm = (): FormState => ({
  title: "",
  source: "other",
  status: "new",
  notes: "",
  company_id: null,
  contact_id: null,
})

const form = ref<FormState>(emptyForm())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    form.value = c
      ? {
          title: c.title,
          source: c.source,
          status: c.status,
          notes: c.notes,
          company_id: c.company?.id ?? null,
          contact_id: c.contact?.id ?? null,
        }
      : emptyForm()
  },
  { immediate: true },
)

// --- Mutation ---

const { mutate: save, isPending } = useMutation({
  mutationFn: () =>
    props.editing
      ? leadsApi.update(props.editing.id, form.value)
      : leadsApi.create(form.value),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: leadKeys.all })
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

  if (!form.value.title.trim()) {
    fieldErrors.value.title = [t("leads.form.title_required")]
    return
  }
  save()
}

const err = (key: string): string | null => fieldErrors.value[key]?.[0] ?? null
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('leads.edit_title') : $t('leads.new')"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <div>
        <label class="text-sm font-medium">{{ $t("leads.form.title") }} *</label>
        <Input
          v-model="form.title"
          :class="err('title') && 'border-rose-500'"
        />
        <p v-if="err('title')" class="text-xs text-rose-600">{{ err("title") }}</p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("leads.form.source") }}</label>
          <Select
            v-model="form.source as LeadSource"
            :options="sourceOptions"
          />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("leads.form.status") }}</label>
          <Select
            v-model="form.status as LeadStatus"
            :options="statusOptions"
          />
        </div>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("leads.form.company") }}</label>
        <Select
          v-model="form.company_id"
          :options="companyOptions"
          :placeholder="$t('leads.form.no_company')"
        />
        <p v-if="err('company_id')" class="text-xs text-rose-600">
          {{ err("company_id") }}
        </p>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("leads.form.notes") }}</label>
        <Textarea v-model="form.notes" :rows="3" />
        <p v-if="err('notes')" class="text-xs text-rose-600">{{ err("notes") }}</p>
      </div>

      <p
        v-if="generalError"
        class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
      >
        {{ generalError }}
      </p>
    </div>

    <template #actions>
      <Button variant="outline" @click="emit('close')">
        {{ $t("common.cancel") }}
      </Button>
      <Button :disabled="isPending" @click="submit">
        <Spinner v-if="isPending" size="sm" />
        <span v-else>{{ $t("common.save") }}</span>
      </Button>
    </template>
  </FormModal>
</template>