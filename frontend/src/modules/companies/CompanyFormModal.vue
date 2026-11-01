<script setup lang="ts">
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { FormModal } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { Textarea } from "@/shared/components/ui/textarea"

import { companiesApi, companyKeys } from "./api"
import type { Company, CompanyWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Company | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; saved: [] }>()
const { t } = useI18n()
const queryClient = useQueryClient()

const emptyForm = (): CompanyWritePayload => ({
  name: "",
  industry: "",
  website: "",
  phone: "",
  email: "",
  address: "",
  city: "",
  country: "",
  notes: "",
})

const form = ref<CompanyWritePayload>(emptyForm())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    if (c) {
      form.value = {
        name: c.name,
        industry: c.industry,
        website: c.website,
        phone: c.phone,
        email: c.email,
        address: c.address,
        city: c.city,
        country: c.country,
        notes: c.notes,
      }
    } else {
      form.value = emptyForm()
    }
  },
  { immediate: true },
)

const { mutate: save, isPending } = useMutation({
  mutationFn: () => {
    const payload = { ...form.value }
    return props.editing
      ? companiesApi.update(props.editing.id, payload)
      : companiesApi.create(payload)
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: companyKeys.all })
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
  if (!form.value.name.trim()) {
    fieldErrors.value.name = [t("companies.form.name_required")]
    return
  }
  save()
}

const err = (k: string) => fieldErrors.value[k]?.[0] ?? null
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('companies.edit_title') : $t('companies.new')"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <div>
        <label class="text-sm font-medium">{{ $t("companies.form.name") }} *</label>
        <Input v-model="form.name" :class="err('name') && 'border-rose-500'" />
        <p v-if="err('name')" class="text-xs text-rose-600">{{ err("name") }}</p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.industry") }}</label>
          <Input v-model="form.industry" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.website") }}</label>
          <Input v-model="form.website" type="url" placeholder="https://" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.phone") }}</label>
          <Input v-model="form.phone" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.email") }}</label>
          <Input v-model="form.email" type="email" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.city") }}</label>
          <Input v-model="form.city" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("companies.form.country") }}</label>
          <Input v-model="form.country" />
        </div>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("companies.form.address") }}</label>
        <Textarea v-model="form.address" :rows="2" />
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("companies.form.notes") }}</label>
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