<script setup lang="ts">
import { computed } from "vue"

import type { FunnelRow } from "../types"

const props = defineProps<{ rows: FunnelRow[] }>()

const maxCount = computed(() =>
  Math.max(1, ...props.rows.map((r) => r.count)),
)

const totalValue = computed(() =>
  props.rows.reduce((s, r) => s + Number(r.total || 0), 0),
)
</script>

<template>
  <div class="space-y-3">
    <div v-if="props.rows.length === 0" class="py-8 text-center text-sm text-slate-500">
      {{ $t("dashboard.empty") }}
    </div>

    <div v-for="row in props.rows" :key="row.stage_id" class="space-y-1">
      <div class="flex items-center justify-between text-sm">
        <span class="font-medium text-slate-700 dark:text-slate-300">{{ row.name }}</span>
        <span class="text-slate-500">
          {{ row.count }} · {{ Number(row.total).toLocaleString() }}
        </span>
      </div>
      <div class="h-3 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div
          class="h-full rounded-full transition-all"
          :style="{
            width: `${Math.max((row.count / maxCount) * 100, 4)}%`,
            backgroundColor: row.color,
          }"
        />
      </div>
    </div>

    <div
      v-if="props.rows.length > 0"
      class="flex justify-between border-t border-slate-100 pt-3 text-sm dark:border-slate-800"
    >
      <span class="text-slate-500">{{ $t("dashboard.funnel_total") }}</span>
      <span class="font-semibold">{{ totalValue.toLocaleString() }}</span>
    </div>
  </div>
</template>