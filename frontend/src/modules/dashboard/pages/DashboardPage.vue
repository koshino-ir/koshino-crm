<script setup lang="ts">
import { useAuthStore } from "@/core/stores/auth"
import { Card } from "@/shared/components/ui/card"
import { AppLayout } from "@/shared/layouts"

const auth = useAuthStore()
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-6xl space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("nav.dashboard") }}
        </h1>
        <p class="text-sm text-slate-500">
          {{ $t("auth.welcome") }}, {{ auth.user?.first_name || auth.user?.email }}
        </p>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card class="p-4">
          <div class="text-sm text-slate-500">{{ $t("nav.deals") }}</div>
          <div class="text-2xl font-bold text-slate-900 dark:text-slate-100">—</div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-slate-500">{{ $t("nav.companies") }}</div>
          <div class="text-2xl font-bold text-slate-900 dark:text-slate-100">—</div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-slate-500">{{ $t("nav.tasks") }}</div>
          <div class="text-2xl font-bold text-slate-900 dark:text-slate-100">—</div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-slate-500">{{ $t("nav.invoices") }}</div>
          <div class="text-2xl font-bold text-slate-900 dark:text-slate-100">—</div>
        </Card>
      </div>

      <Card class="p-6">
        <p class="text-sm text-slate-500">
          Phase 6.2 complete — Layout, i18n, RTL, and Auth are ready.
          Next: Deals module with Kanban.
        </p>
      </Card>
    </div>
  </AppLayout>
</template>