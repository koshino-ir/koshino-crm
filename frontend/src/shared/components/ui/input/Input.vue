<script setup lang="ts">
import { cn } from "@/core/utils/cn"

interface Props {
  modelValue?: string
  type?: string
  placeholder?: string
  disabled?: boolean
  autocomplete?: string
  required?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: "text",
  disabled: false,
  required: false,
})

const emit = defineEmits<{
  "update:modelValue": [value: string]
}>()

function onInput(e: Event) {
  emit("update:modelValue", (e.target as HTMLInputElement).value)
}
</script>

<template>
  <input
    :id="props.id"
    :type="props.type"
    :value="props.modelValue"
    :placeholder="props.placeholder"
    :disabled="props.disabled"
    :autocomplete="props.autocomplete"
    :required="props.required"
    :class="
      cn(
        'flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm',
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