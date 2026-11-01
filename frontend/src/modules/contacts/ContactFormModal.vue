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

import { contactKeys, contactsApi } from "./api"
import type { Contact, ContactWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Contact | null
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
  (companiesData.value?.items ?? []).map((c) => ({
    value: c.id,
    label: c.name,
  })),
)

const empty = (): ContactWritePayload & { company_id: string | null } => ({
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  position: "",
  is_primary: false,
  company_id: null,
})

const form = ref(empty())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    form.value = c
      ? {
          first_name: c.first_name,
          last_name: c.last_name,
          email: c.email,
          phone: c.phone,
          position: c.position,
          is_primary: c.is_primary,
          company_id: c.company?.id ?? null,
        }
      : empty()
  },
  { immediate: true },
)

const { mutate: save, isPending } = useMutation({
  mutationFn: () =>
    props.editing
      ? contactsApi.update(props.editing.id, form.value)
      : contactsApi.create(form.value),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: contactKeys.all })
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
  if (!form.value.first_name.trim()) {
    fieldErrors.value.first_name = [t("contacts.form.first_name_required")]
    return
  }
  save()
}

const err = (k: string) => fieldErrors.value[k]?.[0] ?? null
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('contacts.edit_title') : $t('contacts.new')"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.first_name") }} *</label>
          <Input v-model="form.first_name" :class="err('first_name') && 'border-rose-500'" />
          <p v-if="err('first_name')" class="text-xs text-rose-600">{{ err("first_name") }}</p>
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.last_name") }}</label>
          <Input v-model="form.last_name" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.email") }}</label>
          <Input v-model="form.email" type="email" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.phone") }}</label>
          <Input v-model="form.phone" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.position") }}</label>
          <Input v-model="form.position" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("contacts.form.company") }}</label>
          <Select
            v-model="form.company_id"
            :options="companyOptions"
            :placeholder="$t('contacts.form.no_company')"
          />
        </div>
      </div>

      <label class="flex items-center gap-2 text-sm">
        <input v-model="form.is_primary" type="checkbox" class="h-4 w-4 rounded border-slate-300" />
        {{ $t("contacts.form.is_primary") }}
      </label>

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