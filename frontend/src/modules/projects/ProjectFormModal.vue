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

import { projectKeys, projectsApi } from "./api"
import type { Project, ProjectStatus, ProjectWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Project | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; saved: [] }>()
const { t } = useI18n()
const queryClient = useQueryClient()

const { data: companiesData } = useQuery({
  queryKey: companyKeys.list({ page_size: 100 }),
  queryFn: () => companiesApi.list({ page_size: 100 }),
})

const companyOptions = computed(() =>
  (companiesData.value?.items ?? []).map((c) => ({ value: c.id, label: c.name })),
)

const statusOptions = computed(() => [
  { value: "planning", label: t("projects.statuses.planning") },
  { value: "active", label: t("projects.statuses.active") },
  { value: "on_hold", label: t("projects.statuses.on_hold") },
  { value: "completed", label: t("projects.statuses.completed") },
  { value: "cancelled", label: t("projects.statuses.cancelled") },
])

interface FormState extends Omit<ProjectWritePayload, "client_company_id"> {
  client_company_id: string | null
}

const empty = (): FormState => ({
  name: "",
  description: "",
  status: "planning",
  start_date: null,
  end_date: null,
  budget: "0",
  client_company_id: null,
})

const form = ref<FormState>(empty())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    form.value = c
      ? {
          name: c.name,
          description: c.description,
          status: c.status,
          start_date: c.start_date,
          end_date: c.end_date,
          budget: c.budget,
          client_company_id: c.client_company.id,
        }
      : empty()
  },
  { immediate: true },
)

const { mutate: save, isPending } = useMutation({
  mutationFn: () => {
    // Build an explicit payload so TS knows client_company_id is not null.
    // `submit()` already guarantees it, so the assertion is safe here.
    const payload: ProjectWritePayload = {
      name: form.value.name,
      description: form.value.description,
      status: form.value.status,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      budget: form.value.budget,
      client_company_id: form.value.client_company_id!,
    }
    return props.editing
      ? projectsApi.update(props.editing.id, payload)
      : projectsApi.create(payload)
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: projectKeys.all })
    emit("saved")
  },
  onError: (err) => {
    if (err instanceof ApiError) {
      fieldErrors.value = err.fieldErrors()
      generalError.value = err.firstError()
    }
  },
})

function submit() {
  generalError.value = ""
  fieldErrors.value = {}
  if (!form.value.name.trim()) {
    fieldErrors.value.name = [t("projects.form.name_required")]
    return
  }
  if (!form.value.client_company_id) {
    fieldErrors.value.client_company_id = [t("projects.form.client_required")]
    return
  }
  save()
}

const err = (k: string) => fieldErrors.value[k]?.[0] ?? null
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('projects.edit_title') : $t('projects.new')"
    max-width="lg"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <div>
        <label class="text-sm font-medium">{{ $t("projects.form.name") }} *</label>
        <Input v-model="form.name" :class="err('name') && 'border-rose-500'" />
        <p v-if="err('name')" class="text-xs text-rose-600">{{ err("name") }}</p>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("projects.form.client") }} *</label>
        <Select
          v-model="form.client_company_id"
          :options="companyOptions"
          :placeholder="$t('projects.form.select_client')"
        />
        <p v-if="err('client_company_id')" class="text-xs text-rose-600">
          {{ err("client_company_id") }}
        </p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("projects.form.status") }}</label>
          <Select
            :model-value="form.status ?? 'planning'"
            :options="statusOptions"
            @update:model-value="(v) => (form.status = (v ?? 'planning') as ProjectStatus)"
          />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("projects.form.budget") }}</label>
          <Input v-model="form.budget" type="number" min="0" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("projects.form.start") }}</label>
          <Input v-model="form.start_date as string" type="date" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("projects.form.end") }}</label>
          <Input v-model="form.end_date as string" type="date" />
        </div>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("projects.form.description") }}</label>
        <Textarea v-model="form.description" :rows="2" />
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