<script setup lang="ts">
import { useQuery } from "@tanstack/vue-query"
import { Plus } from "lucide-vue-next"
import { computed, ref } from "vue"

import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { Spinner } from "@/shared/components/ui/spinner"
import { AppLayout } from "@/shared/layouts"

import { dealsApi, pipelinesApi } from "../api"
import { dealKeys, pipelineKeys } from "../api/keys"
import DealFormModal from "../components/DealFormModal.vue"
import KanbanBoard from "../components/KanbanBoard.vue"

const showForm = ref(false)
const selectedPipelineId = ref<string | null>(null)

const { data: pipelines, isLoading: pipelinesLoading } = useQuery({
  queryKey: pipelineKeys.all,
  queryFn: async () => {
    const list = await pipelinesApi.list()
    if (list.length === 0) {
      // Auto-provision default pipeline on first visit
      const created = await pipelinesApi.ensureDefault()
      return [created]
    }
    return list
  },
})

const activePipeline = computed(() => {
  if (!pipelines.value?.length) return null
  const id = selectedPipelineId.value
  if (id) {
    const found = pipelines.value.find((p) => p.id === id)
    if (found) return found
  }
  return pipelines.value.find((p) => p.is_default) ?? pipelines.value[0]
})

const { data: board, isLoading: boardLoading } = useQuery({
  queryKey: computed(() =>
    activePipeline.value
      ? dealKeys.kanban(activePipeline.value.id)
      : (["deals", "kanban", "none"] as const),
  ),
  queryFn: () => dealsApi.kanban(activePipeline.value!.id),
  enabled: computed(() => !!activePipeline.value),
})
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-7xl space-y-6">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("nav.deals") }}
          </h1>
          <p class="text-sm text-slate-500">{{ $t("deals.subtitle") }}</p>
        </div>
        <Button @click="showForm = true">
          <Plus class="h-4 w-4" />
          {{ $t("deals.new") }}
        </Button>
      </div>

      <!-- Pipeline tabs (only shown when >1) -->
      <div
        v-if="pipelines && pipelines.length > 1"
        class="flex gap-1 border-b border-slate-200 dark:border-slate-800"
      >
        <button
          v-for="p in pipelines"
          :key="p.id"
          class="border-b-2 px-4 py-2 text-sm font-medium transition-colors"
          :class="
            activePipeline?.id === p.id
              ? 'border-primary-600 text-primary-700 dark:text-primary-300'
              : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-slate-100'
          "
          @click="selectedPipelineId = p.id"
        >
          {{ p.name }}
        </button>
      </div>

      <div v-if="pipelinesLoading || boardLoading" class="flex justify-center py-12">
        <Spinner />
      </div>

      <KanbanBoard v-else-if="board" :board="board" />

      <Card v-else class="p-8 text-center">
        <p class="text-slate-500">{{ $t("deals.empty") }}</p>
      </Card>
    </div>

    <DealFormModal
      v-if="showForm"
      :pipeline="activePipeline"
      @close="showForm = false"
      @created="showForm = false"
    />
  </AppLayout>
</template>