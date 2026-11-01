<script setup lang="ts">
import { ChevronLeft, ChevronRight } from "lucide-vue-next"
import { computed } from "vue"

interface Props {
  page: number
  totalPages: number
  total: number
}

const props = defineProps<Props>()
const emit = defineEmits<{ change: [page: number] }>()

const canPrev = computed(() => props.page > 1)
const canNext = computed(() => props.page < props.totalPages)

function go(n: number) {
  if (n >= 1 && n <= props.totalPages && n !== props.page) emit("change", n)
}
</script>

<template>
  <div
    v-if="props.totalPages > 1"
    class="flex items-center justify-between gap-4 pt-3 text-sm text-slate-600 dark:text-slate-400"
  >
    <span>{{ props.total }} total</span>
    <div class="flex items-center gap-1">
      <button
        :disabled="!canPrev"
        class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-slate-200 disabled:opacity-40 dark:border-slate-700"
        @click="go(props.page - 1)"
      >
        <ChevronLeft class="h-4 w-4 rtl:rotate-180" />
      </button>
      <span class="px-2">{{ props.page }} / {{ props.totalPages }}</span>
      <button
        :disabled="!canNext"
        class="inline-flex h-8 w-8 items-center justify-center rounded-md border border-slate-200 disabled:opacity-40 dark:border-slate-700"
        @click="go(props.page + 1)"
      >
        <ChevronRight class="h-4 w-4 rtl:rotate-180" />
      </button>
    </div>
  </div>
</template>