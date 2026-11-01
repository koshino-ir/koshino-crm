<script setup lang="ts">
import { Button } from "@/shared/components/ui/button"
import { Spinner } from "@/shared/components/ui/spinner"

interface Props {
  open: boolean
  title: string
  message: string
  confirmLabel?: string
  cancelLabel?: string
  loading?: boolean
  destructive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  confirmLabel: "Confirm",
  cancelLabel: "Cancel",
  loading: false,
  destructive: true,
})
const emit = defineEmits<{ confirm: []; cancel: [] }>()
</script>

<template>
  <div
    v-if="props.open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    @click.self="emit('cancel')"
  >
    <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-slate-900">
      <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100">{{ props.title }}</h2>
      <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">{{ props.message }}</p>
      <div class="mt-6 flex justify-end gap-2">
        <Button variant="outline" :disabled="props.loading" @click="emit('cancel')">
          {{ props.cancelLabel }}
        </Button>
        <Button
          :variant="props.destructive ? 'destructive' : 'default'"
          :disabled="props.loading"
          @click="emit('confirm')"
        >
          <Spinner v-if="props.loading" size="sm" />
          <span v-else>{{ props.confirmLabel }}</span>
        </Button>
      </div>
    </div>
  </div>
</template>