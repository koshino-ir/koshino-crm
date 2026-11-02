<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError, api } from "@/core/api/client"
import { useAuthStore } from "@/core/stores/auth"
import { useCurrentOrg } from "@/core/stores/organization"
import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { AppLayout } from "@/shared/layouts"

interface OrgDetail {
  id: string
  name: string
  slug: string
  timezone: string
  default_currency: string
  default_language: string
}

interface Member {
  id: string
  role: "owner" | "admin" | "member"
  is_active: boolean
  user: { id: string; email: string; first_name: string; last_name: string; avatar: string | null }
}

const { t } = useI18n()
const auth = useAuthStore()
const currentOrg = useCurrentOrg()
const queryClient = useQueryClient()

const orgId = ref<string | null>(null)
watch(currentOrg, (o) => (orgId.value = o?.id ?? null), { immediate: true })

const { data: org, isLoading: orgLoading } = useQuery({
  queryKey: ["settings", "org", orgId],
  queryFn: async () => {
    const { data } = await api.get<OrgDetail>(`/organizations/${orgId.value}/`)
    return data
  },
  enabled: () => !!orgId.value,
})

const { data: members, isLoading: membersLoading } = useQuery({
  queryKey: ["settings", "members", orgId],
  queryFn: async () => {
    const { data } = await api.get<Member[]>(`/organizations/${orgId.value}/members/`)
    return data
  },
  enabled: () => !!orgId.value,
})

// --- Org form ---

const form = ref({ name: "", timezone: "", default_currency: "", default_language: "" })
watch(org, (o) => {
  if (o) {
    form.value = {
      name: o.name,
      timezone: o.timezone,
      default_currency: o.default_currency,
      default_language: o.default_language,
    }
  }
})

const saveError = ref("")
const saveSuccess = ref(false)

const { mutate: saveOrg, isPending: savingOrg } = useMutation({
  mutationFn: async () => {
    const { data } = await api.patch<OrgDetail>(
      `/organizations/${orgId.value}/`,
      form.value,
    )
    return data
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["settings"] })
    saveSuccess.value = true
    setTimeout(() => (saveSuccess.value = false), 2000)
  },
  onError: (err) => {
    saveError.value = err instanceof ApiError ? err.firstError() : t("common.error")
  },
})

// --- Profile language ---

const preferredLanguage = ref<string>(auth.user?.language ?? "fa")
const { mutate: saveLanguage, isPending: savingLang } = useMutation({
  mutationFn: async () => {
    const { data } = await api.patch("/auth/me/", { language: preferredLanguage.value })
    return data
  },
  onSuccess: async () => {
    await auth.init()
  },
})
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("nav.settings") }}
        </h1>
        <p class="text-sm text-slate-500">{{ $t("settings.subtitle") }}</p>
      </div>

      <!-- Organization -->
      <Card class="p-6">
        <h2 class="mb-4 text-base font-semibold">{{ $t("settings.org_title") }}</h2>
        <div v-if="orgLoading" class="flex justify-center py-4"><Spinner /></div>
        <form v-else class="space-y-3" @submit.prevent="saveOrg()">
          <div>
            <label class="text-sm font-medium">{{ $t("settings.form.name") }}</label>
            <Input v-model="form.name" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-sm font-medium">{{ $t("settings.form.timezone") }}</label>
              <Input v-model="form.timezone" placeholder="Asia/Tehran" />
            </div>
            <div>
              <label class="text-sm font-medium">{{ $t("settings.form.currency") }}</label>
              <Input v-model="form.default_currency" placeholder="IRR" />
            </div>
          </div>
          <p v-if="saveError" class="text-sm text-rose-600">{{ saveError }}</p>
          <p v-if="saveSuccess" class="text-sm text-emerald-600">
            {{ $t("settings.saved") }}
          </p>
          <div class="flex justify-end">
            <Button type="submit" :disabled="savingOrg">
              <Spinner v-if="savingOrg" size="sm" />
              <span v-else>{{ $t("common.save") }}</span>
            </Button>
          </div>
        </form>
      </Card>

      <!-- Members -->
      <Card class="p-6">
        <h2 class="mb-4 text-base font-semibold">{{ $t("settings.members_title") }}</h2>
        <div v-if="membersLoading" class="flex justify-center py-4"><Spinner /></div>
        <ul v-else class="divide-y divide-slate-100 dark:divide-slate-800">
          <li
            v-for="m in members ?? []"
            :key="m.id"
            class="flex items-center justify-between py-2"
          >
            <div>
              <div class="font-medium">{{ m.user.first_name }} {{ m.user.last_name }}</div>
              <div class="text-xs text-slate-500">{{ m.user.email }}</div>
            </div>
            <span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs uppercase dark:bg-slate-800">
              {{ $t(`settings.roles.${m.role}`) }}
            </span>
          </li>
        </ul>
      </Card>

      <!-- Language preference -->
      <Card class="p-6">
        <h2 class="mb-4 text-base font-semibold">{{ $t("settings.language_title") }}</h2>
        <div class="space-y-2">
          <select
            v-model="preferredLanguage"
            class="flex h-10 w-full max-w-xs rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="fa">فارسی</option>
            <option value="en">English</option>
            <option value="ar">العربية</option>
          </select>
          <div>
            <Button :disabled="savingLang" @click="saveLanguage()">
              <Spinner v-if="savingLang" size="sm" />
              <span v-else>{{ $t("common.save") }}</span>
            </Button>
          </div>
        </div>
      </Card>
    </div>
  </AppLayout>
</template>