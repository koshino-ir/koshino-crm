<script setup lang="ts">
import { cn } from "@/core/utils/cn"
</script>

<template>
  <div
    :class="
      cn(
        'rounded-lg border border-slate-200 bg-white shadow-sm',
        'dark:border-slate-800 dark:bg-slate-900',
        $attrs.class as string,
      )
    "
  >
    <slot />
  </div>
</template>