<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import { VueDraggable } from "vue-draggable-plus"

import type { Deal, Stage } from "../types"
import { translateStage } from "../utils/stageLabel"
import DealCard from "./DealCard.vue"

interface Props {
  stage: Stage
}

const props = defineProps<Props>()
const emit = defineEmits<{
  move: [payload: { dealId: string; toStageId: string; toIndex: number }]
}>()

const { t } = useI18n()

const stageLabel = computed(() => translateStage(props.stage.name, t))

const deals = ref<Deal[]>([])

watch(
  () => props.stage.deals,
  (newVal) => {
    deals.value = [...newVal]
  },
  { immediate: true },
)

const total = computed(() =>
  deals.value.reduce((sum, d) => sum + Number(d.amount || 0), 0),
)

function onAdd(event: { newIndex?: number }) {
  if (event.newIndex === undefined) return
  const moved = deals.value[event.newIndex]
  if (!moved) return
  emit("move", {
    dealId: moved.id,
    toStageId: props.stage.id,
    toIndex: event.newIndex,
  })
}

function onUpdate(event: { newIndex?: number }) {
  if (event.newIndex === undefined) return
  const moved = deals.value[event.newIndex]
  if (!moved) return
  emit("move", {
    dealId: moved.id,
    toStageId: props.stage.id,
    toIndex: event.newIndex,
  })
}
</script>

<template>
  <div class="flex w-72 shrink-0 flex-col rounded-lg bg-slate-100 dark:bg-slate-900/60">
    <div class="flex items-center justify-between border-b border-slate-200 px-3 py-2 dark:border-slate-800">
      <div class="flex items-center gap-2">
        <span
          class="inline-block h-2.5 w-2.5 rounded-full"
          :style="{ backgroundColor: stage.color }"
        />
        <span class="text-sm font-semibold text-slate-800 dark:text-slate-100">
          {{ stageLabel }}
        </span>
        <span class="text-xs text-slate-500">({{ deals.length }})</span>
      </div>
      <span class="text-xs font-medium text-slate-600 dark:text-slate-400">
        {{ total.toLocaleString() }}
      </span>
    </div>

    <VueDraggable
      v-model="deals"
      :group="{ name: 'deals', pull: true, put: true }"
      :animation="200"
      :delay="100"
      :delay-on-touch-only="false"
      ghost-class="dragging-ghost"
      drag-class="dragging"
      class="flex min-h-[120px] flex-1 flex-col gap-2 overflow-y-auto p-2"
      @add="onAdd"
      @update="onUpdate"
    >
      <DealCard v-for="deal in deals" :key="deal.id" :deal="deal" />
</VueDraggable>
  </div>
</template>

<style scoped>
  .dragging-ghost {
    opacity: 0.4;
  }
  .dragging {
    transform: rotate(1.5deg);
    box-shadow: 0 8px 24px -4px rgba(79, 70, 229, 0.25);
  }
</style>