<script setup lang="ts">
import { cn } from "@/core/utils/cn"

interface Props {
  modelValue?: string
  placeholder?: string
  rows?: number
  disabled?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), { rows: 3 })
const emit = defineEmits<{ "update:modelValue": [v: string] }>()

function onInput(e: Event) {
  emit("update:modelValue", (e.target as HTMLTextAreaElement).value)
}
</script>

<template>
  <textarea
    :id="props.id"
    :value="props.modelValue"
    :placeholder="props.placeholder"
    :rows="props.rows"
    :disabled="props.disabled"
    :class="
      cn(
        'flex w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm',
        'placeholder:text-slate-400',
        'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder:text-slate-500',
        $attrs.class as string,
      )
    "
    @input="onInput"
  />
</template>