<script setup lang="ts">
import { useQuery } from "@tanstack/vue-query"
import {
  Building2,
  CheckCircle2,
  Clock,
  DollarSign,
  Kanban,
  UserSquare2,
} from "lucide-vue-next"
import { computed } from "vue"

import { Card } from "@/shared/components/ui/card"
import { Spinner } from "@/shared/components/ui/spinner"
import { AppLayout } from "@/shared/layouts"

import { dashboardApi, dashboardKeys } from "./api"
import FunnelChart from "./components/FunnelChart.vue"
import KpiCard from "./components/KpiCard.vue"
import RevenueChart from "./components/RevenueChart.vue"
import type { RecentActivity } from "./types"

const { data: stats, isLoading: statsLoading } = useQuery({
  queryKey: dashboardKeys.stats,
  queryFn: () => dashboardApi.stats(),
})

const { data: funnel, isLoading: funnelLoading } = useQuery({
  queryKey: dashboardKeys.funnel,
  queryFn: () => dashboardApi.funnel(),
})

const { data: revenue, isLoading: revenueLoading } = useQuery({
  queryKey: dashboardKeys.revenue(6),
  queryFn: () => dashboardApi.revenue(6),
})

const { data: recent, isLoading: recentLoading } = useQuery({
  queryKey: dashboardKeys.recent,
  queryFn: () => dashboardApi.recentActivities(),
})

const typeIcons: Record<RecentActivity["type"], string> = {
  call: "📞",
  email: "✉️",
  meeting: "🤝",
  note: "📝",
}

const money = computed(
  () => (v: string | number | undefined) => Number(v ?? 0).toLocaleString(),
)
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-7xl space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("nav.dashboard") }}
        </h1>
        <p class="text-sm text-slate-500">{{ $t("dashboard.subtitle") }}</p>
      </div>

      <!-- KPI row -->
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          :label="$t('dashboard.kpi.open_deals')"
          :value="stats?.open_deals_count ?? '—'"
          :subtitle="stats ? money(stats.open_deals_value) : undefined"
          :icon="Kanban"
          tone="primary"
          :loading="statsLoading"
        />
        <KpiCard
          :label="$t('dashboard.kpi.won')"
          :value="stats?.won_deals_count ?? '—'"
          :subtitle="stats ? money(stats.won_deals_value) : undefined"
          :icon="DollarSign"
          tone="success"
          :loading="statsLoading"
        />
        <KpiCard
          :label="$t('dashboard.kpi.companies')"
          :value="stats?.companies_count ?? '—'"
          :icon="Building2"
          tone="info"
          :loading="statsLoading"
        />
        <KpiCard
          :label="$t('dashboard.kpi.leads')"
          :value="stats?.leads_count ?? '—'"
          :icon="UserSquare2"
          tone="warning"
          :loading="statsLoading"
        />
      </div>

      <!-- Second row: tasks / charts -->
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          :label="$t('dashboard.kpi.tasks_open')"
          :value="stats?.tasks_open_count ?? '—'"
          :icon="Clock"
          tone="info"
          :loading="statsLoading"
        />
        <KpiCard
          :label="$t('dashboard.kpi.tasks_overdue')"
          :value="stats?.tasks_overdue_count ?? '—'"
          :icon="CheckCircle2"
          tone="danger"
          :loading="statsLoading"
        />
      </div>

      <!-- Charts row -->
      <div class="grid gap-4 lg:grid-cols-2">
        <Card class="p-6">
          <h2 class="mb-4 text-base font-semibold text-slate-900 dark:text-slate-100">
            {{ $t("dashboard.funnel") }}
          </h2>
          <div v-if="funnelLoading" class="flex justify-center py-8">
            <Spinner />
          </div>
          <FunnelChart v-else :rows="funnel ?? []" />
        </Card>

        <Card class="p-6">
          <h2 class="mb-4 text-base font-semibold text-slate-900 dark:text-slate-100">
            {{ $t("dashboard.revenue") }}
          </h2>
          <div v-if="revenueLoading" class="flex justify-center py-8">
            <Spinner />
          </div>
          <RevenueChart v-else :rows="revenue ?? []" />
        </Card>
      </div>

      <!-- Recent activities -->
      <Card class="p-6">
        <h2 class="mb-4 text-base font-semibold text-slate-900 dark:text-slate-100">
          {{ $t("dashboard.recent_activities") }}
        </h2>
        <div v-if="recentLoading" class="flex justify-center py-8">
          <Spinner />
        </div>
        <div v-else-if="!recent || recent.length === 0" class="py-8 text-center text-sm text-slate-500">
          {{ $t("dashboard.empty") }}
        </div>
        <ul v-else class="divide-y divide-slate-100 dark:divide-slate-800">
          <li
            v-for="a in recent"
            :key="a.id"
            class="flex items-start gap-3 py-3"
          >
            <span class="text-xl">{{ typeIcons[a.type] }}</span>
            <div class="min-w-0 flex-1">
              <div class="font-medium text-slate-900 dark:text-slate-100 truncate">
                {{ a.subject }}
              </div>
              <div class="text-xs text-slate-500">
                {{ a.created_by?.first_name || a.created_by?.email }} ·
                {{ new Date(a.occurred_at).toLocaleString() }}
              </div>
            </div>
            <span class="text-xs text-slate-400">{{ $t(`activities.types.${a.type}`) }}</span>
          </li>
        </ul>
      </Card>
    </div>
  </AppLayout>
</template>