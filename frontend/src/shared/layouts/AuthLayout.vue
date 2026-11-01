<script setup lang="ts">
import { LangSwitcher, ThemeToggle } from "@/shared/components/layout"
</script>

<template>
  <div
    class="relative flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-primary-50 p-4 dark:from-slate-950 dark:to-slate-900"
  >
    <div class="absolute top-4 end-4 flex gap-2">
      <LangSwitcher />
      <ThemeToggle />
    </div>

    <div class="w-full max-w-md">
      <div class="mb-8 text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-2xl font-bold text-white">
          K
        </div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">Koshino CRM</h1>
      </div>
      <slot />
    </div>
  </div>
</template>