<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"

import { Card } from "@/shared/components/ui/card"
import { AppLayout } from "@/shared/layouts"

const route = useRoute()

const title = computed(() => {
  const meta = route.meta as { titleKey?: string }
  if (meta.titleKey) {
    // $t needs access to i18n — safe to call inside computed
    return meta.titleKey
  }
  return (route.name as string) ?? "Page"
})
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-4xl space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t(title) }}
        </h1>
        <p class="text-sm text-slate-500">
          This module is coming in a future phase.
        </p>
      </div>
      <Card class="p-8 text-center">
        <p class="text-slate-500">🚧 Under construction</p>
      </Card>
    </div>
  </AppLayout>
</template>