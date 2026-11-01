<script setup lang="ts">
import { AppSidebar, AppTopbar } from "@/shared/components/layout"
</script>

<template>
  <div class="flex h-screen bg-slate-50 dark:bg-slate-950">
    <AppSidebar />
    <div class="flex flex-1 flex-col overflow-hidden">
      <AppTopbar />
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>