<script setup lang="ts">
import { cn } from "@/core/utils/cn"
</script>

<template>
  <div :class="cn('animate-pulse rounded-md bg-slate-200 dark:bg-slate-800', $attrs.class as string)" />
</template>