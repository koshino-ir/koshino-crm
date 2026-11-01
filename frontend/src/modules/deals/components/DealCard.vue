<script setup lang="ts">
import { RouterLink } from "vue-router"

import type { Deal } from "../types"

defineProps<{ deal: Deal }>()
</script>

<template>
  <RouterLink
    :to="{ name: 'deal-detail', params: { id: deal.id } }"
    class="block rounded-md border border-slate-200 bg-white p-3 text-sm cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow dark:border-slate-700 dark:bg-slate-800"
    draggable="false"
  >
    <div class="font-medium text-slate-900 dark:text-slate-100 line-clamp-2">
      {{ deal.title }}
    </div>
    <div class="mt-1 text-xs text-slate-500 truncate">
      {{ deal.company.name }}
    </div>
    <div class="mt-2 flex items-center justify-between">
      <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
        {{ Number(deal.amount).toLocaleString() }} {{ deal.currency }}
      </span>
      <span
        v-if="deal.expected_close_date"
        class="text-xs text-slate-400"
      >
        {{ deal.expected_close_date }}
      </span>
    </div>
  </RouterLink>
</template>