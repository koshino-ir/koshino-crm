<script setup lang="ts">
import { ChevronDown, LogOut, Settings, User } from "lucide-vue-next"
import { computed, onBeforeUnmount, onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import { Avatar } from "@/shared/components/ui/avatar"
import { useAuthStore } from "@/core/stores/auth"
import { useOrganizationStore } from "@/core/stores/organization"
import { useQueryClient } from "@tanstack/vue-query"


const queryClient = useQueryClient()
const auth = useAuthStore()
const orgStore = useOrganizationStore()
const router = useRouter()

const open = ref(false)
const root = ref<HTMLElement | null>(null)

const displayName = computed(() => {
  if (!auth.user) return ""
  return `${auth.user.first_name} ${auth.user.last_name}`.trim() || auth.user.email
})

async function logout() {
  await auth.logout()
  orgStore.clear()
  queryClient.clear()
  router.push({ name: "login" })
}

function onDocClick(e: MouseEvent) {
  if (root.value && !root.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener("click", onDocClick))
onBeforeUnmount(() => document.removeEventListener("click", onDocClick))
</script>

<template>
  <div ref="root" class="relative">
    <button
      type="button"
      class="inline-flex items-center gap-2 rounded-md px-2 py-1 hover:bg-slate-100 dark:hover:bg-slate-800"
      @click="open = !open"
    >
      <Avatar :name="displayName" :src="auth.user?.avatar" size="sm" />
      <span class="hidden md:inline text-sm font-medium text-slate-900 dark:text-slate-100">
        {{ displayName }}
      </span>
      <ChevronDown class="hidden md:inline h-3.5 w-3.5 text-slate-500" />
    </button>

    <div
      v-if="open"
      class="absolute end-0 z-50 mt-1 w-52 rounded-md border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-700 dark:bg-slate-900"
    >
      <div class="border-b border-slate-100 px-3 py-2 dark:border-slate-800">
        <div class="truncate text-sm font-medium">{{ displayName }}</div>
        <div class="truncate text-xs text-slate-500">{{ auth.user?.email }}</div>
      </div>
      <button
        class="flex w-full items-center gap-2 px-3 py-2 text-start text-sm hover:bg-slate-50 dark:hover:bg-slate-800"
      >
        <User class="h-4 w-4" />
        {{ $t("layout.profile") }}
      </button>
      <button
        class="flex w-full items-center gap-2 px-3 py-2 text-start text-sm hover:bg-slate-50 dark:hover:bg-slate-800"
      >
        <Settings class="h-4 w-4" />
        {{ $t("layout.settings") }}
      </button>
      <button
        class="flex w-full items-center gap-2 px-3 py-2 text-start text-sm text-rose-600 hover:bg-rose-50 dark:text-rose-400 dark:hover:bg-rose-950/30"
        @click="logout"
      >
        <LogOut class="h-4 w-4" />
        {{ $t("auth.logout") }}
      </button>
    </div>
  </div>
</template>