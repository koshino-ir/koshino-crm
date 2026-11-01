<script setup lang="ts">
import { computed } from "vue"

import { useAuthStore } from "@/core/stores/auth"
import { useOrganizationStore } from "@/core/stores/organization"
import { LangSwitcher } from "./index"
import { ThemeToggle } from "./index"
import { UserMenu } from "./index"

const auth = useAuthStore()
const orgStore = useOrganizationStore()

const orgs = computed(() => auth.user?.organizations ?? [])
const currentOrgId = computed(() => orgStore.currentId ?? orgs.value[0]?.id)

function changeOrg(e: Event) {
  const id = (e.target as HTMLSelectElement).value
  orgStore.setCurrent(orgs.value, id)
  // Reload to refetch data with new X-Organization-Id header
  window.location.reload()
}
</script>

<template>
  <header
    class="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 dark:border-slate-800 dark:bg-slate-900"
  >
    <div class="flex items-center gap-3">
      <select
        v-if="orgs.length > 1"
        :value="currentOrgId"
        class="h-9 rounded-md border border-slate-200 bg-white px-2 text-sm dark:border-slate-700 dark:bg-slate-900"
        @change="changeOrg"
      >
        <option v-for="org in orgs" :key="org.id" :value="org.id">
          {{ org.name }}
        </option>
      </select>
      <div v-else-if="orgs[0]" class="text-sm font-medium text-slate-700 dark:text-slate-300">
        {{ orgs[0].name }}
      </div>
    </div>

    <div class="flex items-center gap-2">
      <LangSwitcher />
      <ThemeToggle />
      <UserMenu />
    </div>
  </header>
</template>