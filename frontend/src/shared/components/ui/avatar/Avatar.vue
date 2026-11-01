<script setup lang="ts">
import { computed } from "vue"

import { cn } from "@/core/utils/cn"

interface Props {
  name?: string
  src?: string | null
  size?: "sm" | "md" | "lg"
}

const props = withDefaults(defineProps<Props>(), { size: "md" })

const initials = computed(() => {
  if (!props.name) return "?"
  const parts = props.name.trim().split(/\s+/)
  return (parts[0]?.[0] ?? "") + (parts[1]?.[0] ?? "")
})

const sizeClass = computed(
  () =>
    ({
      sm: "h-8 w-8 text-xs",
      md: "h-10 w-10 text-sm",
      lg: "h-12 w-12 text-base",
    })[props.size],
)
</script>

<template>
  <div
    :class="
      cn(
        'inline-flex items-center justify-center rounded-full bg-primary-600 text-white font-medium select-none overflow-hidden',
        sizeClass,
      )
    "
  >
    <img
      v-if="props.src"
      :src="props.src"
      :alt="props.name ?? ''"
      class="h-full w-full object-cover"
    />
    <span v-else>{{ initials.toUpperCase() }}</span>
  </div>
</template>