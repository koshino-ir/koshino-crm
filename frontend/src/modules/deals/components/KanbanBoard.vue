<script setup lang="ts">
import { useMutation, useQueryClient } from "@tanstack/vue-query"

import { dealsApi } from "../api"
import { dealKeys } from "../api/keys"
import type { KanbanBoard } from "../types"
import KanbanColumn from "./KanbanColumn.vue"

const props = defineProps<{ board: KanbanBoard }>()
const queryClient = useQueryClient()

const { mutate: moveDeal } = useMutation({
  mutationFn: (p: { dealId: string; stageId: string; order: number }) =>
    dealsApi.move(p.dealId, { stage_id: p.stageId, order: p.order }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: dealKeys.all })
  },
  onError: () => {
    // Revert by refetching from server
    queryClient.invalidateQueries({ queryKey: dealKeys.all })
  },
})

function onMove(payload: { dealId: string; toStageId: string; toIndex: number }) {
  moveDeal({
    dealId: payload.dealId,
    stageId: payload.toStageId,
    order: payload.toIndex,
  })
}
</script>

<template>
  <div class="flex gap-4 overflow-x-auto pb-4">
    <KanbanColumn
      v-for="stage in props.board.stages"
      :key="stage.id"
      :stage="stage"
      @move="onMove"
    />
  </div>
</template>