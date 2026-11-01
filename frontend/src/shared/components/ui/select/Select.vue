<script setup lang="ts">
import { cn } from "@/core/utils/cn"

interface Option {
  value: string | null
  label: string
}

interface Props {
  modelValue: string | null
  options: Option[]
  placeholder?: string
  disabled?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{ "update:modelValue": [v: string | null] }>()

function onChange(e: Event) {
  const v = (e.target as HTMLSelectElement).value
  emit("update:modelValue", v === "" ? null : v)
}
</script>

<template>
  <select
    :value="props.modelValue ?? ''"
    :disabled="props.disabled"
    :class="
      cn(
        'flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm',
        'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100',
        $attrs.class as string,
      )
    "
    @change="onChange"
  >
    <option v-if="props.placeholder" value="">{{ props.placeholder }}</option>
    <option v-for="opt in props.options" :key="String(opt.value)" :value="opt.value ?? ''">
      {{ opt.label }}
    </option>
  </select>
</template>