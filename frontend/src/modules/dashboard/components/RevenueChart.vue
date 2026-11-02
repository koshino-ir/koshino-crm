<script setup lang="ts">
import { computed } from "vue"

import type { RevenueRow } from "../types"

const props = defineProps<{ rows: RevenueRow[] }>()

const W = 500
const H = 200
const PAD = 40

interface Chart {
  line: string
  area: string
  max: number
  coords: ReadonlyArray<readonly [number, number]>
}

const points = computed<Chart>(() => {
  const empty: Chart = { line: "", area: "", max: 0, coords: [] }
  if (props.rows.length === 0) return empty

  const max = Math.max(1, ...props.rows.map((r) => Number(r.total)))
  const step = props.rows.length > 1 ? (W - PAD * 2) / (props.rows.length - 1) : 0

  const coords: ReadonlyArray<readonly [number, number]> = props.rows.map((r, i) => {
    const x = PAD + i * step
    const y = H - PAD - (Number(r.total) / max) * (H - PAD * 2)
    return [x, y] as const
  })

  const line = coords.map(([x, y], i) => `${i === 0 ? "M" : "L"} ${x} ${y}`).join(" ")
  const last = coords[coords.length - 1]
  const first = coords[0]
  const area = `${line} L ${last[0]} ${H - PAD} L ${first[0]} ${H - PAD} Z`

  return { line, area, max, coords }
})
</script>

<template>
  <div v-if="props.rows.length === 0" class="py-8 text-center text-sm text-slate-500">
    {{ $t("dashboard.empty") }}
  </div>

  <svg v-else :viewBox="`0 0 ${W} ${H}`" class="w-full" preserveAspectRatio="xMidYMid meet">
    <!-- Grid lines -->
    <line
      v-for="i in 4"
      :key="`g${i}`"
      :x1="PAD"
      :x2="W - PAD"
      :y1="H - PAD - (i * (H - PAD * 2)) / 4"
      :y2="H - PAD - (i * (H - PAD * 2)) / 4"
      stroke="currentColor"
      class="text-slate-100 dark:text-slate-800"
      stroke-width="1"
    />

    <!-- Area -->
    <path :d="points.area" class="fill-primary-100 dark:fill-primary-950/40" />

    <!-- Line -->
    <path
      :d="points.line"
      class="stroke-primary-600"
      fill="none"
      stroke-width="2.5"
      stroke-linecap="round"
      stroke-linejoin="round"
    />

    <!-- Dots -->
    <circle
      v-for="([x, y], i) in points.coords"
      :key="`d${i}`"
      :cx="x"
      :cy="y"
      r="4"
      class="fill-primary-600 stroke-white dark:stroke-slate-900"
      stroke-width="2"
    />

    <!-- X labels -->
    <text
      v-for="(row, i) in props.rows"
      :key="`x${i}`"
      :x="points.coords[i]?.[0] ?? 0"
      :y="H - 10"
      text-anchor="middle"
      class="fill-slate-500 text-[10px]"
    >
      {{ row.month?.slice(5) ?? "" }}
    </text>
  </svg>
</template>