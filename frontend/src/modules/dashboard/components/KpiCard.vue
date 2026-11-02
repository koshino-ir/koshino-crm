<script setup lang="ts">
import type { Component } from "vue"
import { cn } from "@/core/utils/cn"

interface Props {
  label: string
  value: string | number
  subtitle?: string
  icon: Component
  tone?: "primary" | "success" | "warning" | "danger" | "info"
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), { tone: "primary", loading: false })

const toneClasses = {
  primary: "bg-primary-50 text-primary-600 dark:bg-primary-950/40 dark:text-primary-400",
  success: "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/40 dark:text-emerald-400",
  warning: "bg-amber-50 text-amber-600 dark:bg-amber-950/40 dark:text-amber-400",
  danger: "bg-rose-50 text-rose-600 dark:bg-rose-950/40 dark:text-rose-400",
  info: "bg-sky-50 text-sky-600 dark:bg-sky-950/40 dark:text-sky-400",
}
</script>

<template>
  <div
    class="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="min-w-0">
        <div class="text-sm text-slate-500 truncate">{{ props.label }}</div>
        <div
          v-if="props.loading"
          class="mt-2 h-7 w-24 animate-pulse rounded bg-slate-200 dark:bg-slate-800"
        />
        <div v-else class="mt-1 text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ props.value }}
        </div>
        <div v-if="props.subtitle" class="mt-1 text-xs text-slate-500">
          {{ props.subtitle }}
        </div>
      </div>
      <div :class="cn('rounded-md p-2', toneClasses[props.tone])">
        <component :is="props.icon" class="h-5 w-5" />
      </div>
    </div>
  </div>
</template>