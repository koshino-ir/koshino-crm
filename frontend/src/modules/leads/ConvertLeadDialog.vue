<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { ref } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { pipelinesApi } from "@/modules/deals/api"
import { dealKeys, pipelineKeys } from "@/modules/deals/api/keys"
import { Button } from "@/shared/components/ui/button"
import { Select } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"

import { leadKeys, leadsApi } from "./api"
import type { Lead } from "./types"

interface Props {
  open: boolean
  lead: Lead | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; converted: [] }>()
const { t } = useI18n()
const queryClient = useQueryClient()

const pipelineId = ref<string | null>(null)
const error = ref("")

const { data: pipelines } = useQuery({
  queryKey: pipelineKeys.all,
  queryFn: async () => {
    const list = await pipelinesApi.list()
    if (list.length === 0) {
      const created = await pipelinesApi.ensureDefault()
      return [created]
    }
    if (!pipelineId.value) pipelineId.value = list.find((p) => p.is_default)?.id ?? list[0].id
    return list
  },
})

const { mutate: convert, isPending } = useMutation({
  mutationFn: () => leadsApi.convert(props.lead!.id, pipelineId.value!),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: leadKeys.all })
    queryClient.invalidateQueries({ queryKey: dealKeys.all })
    emit("converted")
  },
  onError: (err) => {
    error.value = err instanceof ApiError ? err.firstError() : t("common.error")
  },
})

function submit() {
  if (!pipelineId.value) {
    error.value = t("leads.convert.no_pipeline")
    return
  }
  convert()
}
</script>

<template>
  <div
    v-if="props.open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    @click.self="emit('close')"
  >
    <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-slate-900">
      <h2 class="text-lg font-bold">{{ $t("leads.convert.title") }}</h2>
      <p class="mt-1 text-sm text-slate-500">
        {{ $t("leads.convert.subtitle", { title: props.lead?.title ?? "" }) }}
      </p>
      <div class="mt-4 space-y-3">
        <div>
          <label class="text-sm font-medium">{{ $t("leads.convert.pipeline") }}</label>
          <Select
            v-model="pipelineId"
            :options="(pipelines ?? []).map((p) => ({ value: p.id, label: p.name }))"
          />
        </div>
        <p v-if="error" class="text-sm text-rose-600">{{ error }}</p>
      </div>
      <div class="mt-6 flex justify-end gap-2">
        <Button variant="outline" @click="emit('close')">{{ $t("common.cancel") }}</Button>
        <Button :disabled="isPending" @click="submit">
          <Spinner v-if="isPending" size="sm" />
          <span v-else>{{ $t("leads.convert.confirm") }}</span>
        </Button>
      </div>
    </div>
  </div>
</template>