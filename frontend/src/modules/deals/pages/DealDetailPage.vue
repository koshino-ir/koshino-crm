<script setup lang="ts">
import { useQuery } from "@tanstack/vue-query"
import { ArrowLeft } from "lucide-vue-next"
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"

import { Card } from "@/shared/components/ui/card"
import { Spinner } from "@/shared/components/ui/spinner"
import { AppLayout } from "@/shared/layouts"

import { dealsApi } from "../api"
import { dealKeys } from "../api/keys"
import { translateStage } from "../utils/stageLabel"

const route = useRoute()
const { t } = useI18n()
const id = route.params.id as string

const { data: deal, isLoading } = useQuery({
  queryKey: dealKeys.detail(id),
  queryFn: () => dealsApi.retrieve(id),
})

const stageLabel = computed(() =>
  deal.value ? translateStage(deal.value.stage.name, t) : "",
)
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-4xl space-y-6">
      <RouterLink
        :to="{ name: 'deals' }"
        class="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-900 dark:hover:text-slate-100"
      >
        <ArrowLeft class="h-4 w-4 rtl:rotate-180" />
        {{ $t("common.back") }}
      </RouterLink>

      <div v-if="isLoading" class="flex justify-center py-12">
        <Spinner />
      </div>

      <template v-else-if="deal">
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ deal.title }}
        </h1>

        <Card class="p-6">
          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.company") }}</div>
              <div class="font-medium">{{ deal.company.name }}</div>
            </div>
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.amount") }}</div>
              <div class="font-medium">
                {{ Number(deal.amount).toLocaleString() }} {{ deal.currency }}
              </div>
            </div>
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.stage") }}</div>
              <div class="flex items-center gap-2 font-medium">
                <span
                  class="inline-block h-2.5 w-2.5 rounded-full"
                  :style="{ backgroundColor: deal.stage.color }"
                />
                {{ stageLabel }}
              </div>
            </div>
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.status") }}</div>
              <div class="font-medium capitalize">{{ deal.status }}</div>
            </div>
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.probability") }}</div>
              <div class="font-medium">{{ deal.probability }}%</div>
            </div>
            <div>
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.expected_close") }}</div>
              <div class="font-medium">{{ deal.expected_close_date || "—" }}</div>
            </div>
            <div v-if="deal.contact">
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.contact") }}</div>
              <div class="font-medium">
                {{ deal.contact.first_name }} {{ deal.contact.last_name }}
                <span class="text-slate-500">· {{ deal.contact.email }}</span>
              </div>
            </div>
            <div v-if="deal.owner">
              <div class="text-xs uppercase text-slate-500">{{ $t("deals.detail.owner") }}</div>
              <div class="font-medium">
                {{ deal.owner.first_name }} {{ deal.owner.last_name }}
              </div>
            </div>
          </div>
        </Card>

        <p class="text-sm text-slate-500">
          Activities, tasks and edit — coming in next phase.
        </p>
      </template>
    </div>
  </AppLayout>
</template>