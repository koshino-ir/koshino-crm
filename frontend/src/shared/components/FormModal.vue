<script setup lang="ts">
interface Props {
  open: boolean
  title: string
  maxWidth?: "sm" | "md" | "lg"
}

const props = withDefaults(defineProps<Props>(), { maxWidth: "md" })
const emit = defineEmits<{ close: [] }>()

const widthClass = {
  sm: "max-w-sm",
  md: "max-w-lg",
  lg: "max-w-2xl",
}[props.maxWidth]
</script>

<template>
  <div
    v-if="props.open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    @click.self="emit('close')"
  >
    <div :class="['w-full rounded-lg bg-white p-6 shadow-xl dark:bg-slate-900', widthClass]">
      <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100">{{ props.title }}</h2>
      <div class="mt-4">
        <slot />
      </div>
      <div class="mt-6 flex justify-end gap-2">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>