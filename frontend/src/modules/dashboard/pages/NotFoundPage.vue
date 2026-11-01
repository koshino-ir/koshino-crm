<script setup lang="ts">
import { RouterLink } from "vue-router"

import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { AppLayout } from "@/shared/layouts"
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-md mt-12">
      <Card class="p-8 text-center space-y-4">
        <div class="text-5xl font-bold text-primary-600">404</div>
        <p class="text-slate-600 dark:text-slate-400">Page not found</p>
        <RouterLink :to="{ name: 'dashboard' }">
          <Button>Back to dashboard</Button>
        </RouterLink>
      </Card>
    </div>
  </AppLayout>
</template>