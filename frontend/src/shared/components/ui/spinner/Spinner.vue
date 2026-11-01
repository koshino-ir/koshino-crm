<script setup lang="ts">
import { cn } from "@/core/utils/cn"

interface Props {
  size?: "sm" | "md"
}

const props = withDefaults(defineProps<Props>(), { size: "md" })
const sizeClass = props.size === "sm" ? "h-4 w-4 border-2" : "h-6 w-6 border-2"
</script>

<template>
  <span
    :class="
      cn(
        'inline-block animate-spin rounded-full border-current border-t-transparent',
        sizeClass,
      )
    "
  />
</template>