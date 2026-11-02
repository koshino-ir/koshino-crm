<script setup lang="ts">
import {
  BarChart3,
  Building2,
  ChevronLeft,
  FileText,
  Folder,
  Kanban,
  ListChecks,
  MessageSquare,
  Settings,
  Users,
  UserSquare2,
} from "lucide-vue-next"
import type { Component } from "vue"
import { computed } from "vue"
import { RouterLink } from "vue-router"

import { useUiStore } from "@/core/stores/ui"
import { cn } from "@/core/utils/cn"

interface NavItem {
  name: string
  labelKey: string
  icon: Component
}

const items: NavItem[] = [
  { name: "dashboard", labelKey: "nav.dashboard", icon: BarChart3 },
  { name: "deals", labelKey: "nav.deals", icon: Kanban },
  { name: "activities", labelKey: "nav.activities", icon: MessageSquare },
  { name: "companies", labelKey: "nav.companies", icon: Building2 },
  { name: "contacts", labelKey: "nav.contacts", icon: Users },
  { name: "leads", labelKey: "nav.leads", icon: UserSquare2 },
  { name: "tasks", labelKey: "nav.tasks", icon: ListChecks },
  { name: "projects", labelKey: "nav.projects", icon: Folder },
  { name: "invoices", labelKey: "nav.invoices", icon: FileText },
  { name: "settings", labelKey: "nav.settings", icon: Settings },
]

const ui = useUiStore()
const collapsed = computed(() => ui.sidebarCollapsed)
</script>

<template>
  <aside
    :class="
      cn(
        'flex h-screen flex-col border-e border-slate-200 bg-white transition-all duration-200',
        'dark:border-slate-800 dark:bg-slate-900',
        collapsed ? 'w-16' : 'w-64',
      )
    "
  >
    <!-- Brand -->
    <div class="flex h-16 items-center gap-2 border-b border-slate-200 px-4 dark:border-slate-800">
      <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary-600 text-white font-bold">
        K
      </div>
      <span v-if="!collapsed" class="text-lg font-semibold text-slate-900 dark:text-slate-100">
        Koshino
      </span>
    </div>

    <!-- Nav -->
    <nav class="flex-1 space-y-1 overflow-y-auto p-2">
      <RouterLink
        v-for="item in items"
        :key="item.name"
        :to="{ name: item.name }"
        custom
        v-slot="{ isActive, navigate, href }"
      >
        <a
          :href="href"
          :class="
            cn(
              'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
              collapsed && 'justify-center px-2',
              isActive
                ? 'bg-primary-50 text-primary-700 dark:bg-primary-950/40 dark:text-primary-300'
                : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800',
            )
          "
          @click="navigate"
        >
          <component :is="item.icon" class="h-5 w-5 shrink-0" />
          <span v-if="!collapsed">{{ $t(item.labelKey) }}</span>
        </a>
      </RouterLink>
    </nav>

    <!-- Collapse toggle -->
    <button
      class="flex h-12 items-center justify-center border-t border-slate-200 text-slate-500 hover:bg-slate-100 dark:border-slate-800 dark:hover:bg-slate-800"
      :aria-label="collapsed ? $t('layout.expand') : $t('layout.collapse')"
      @click="ui.toggleSidebar()"
    >
      <ChevronLeft
        class="h-5 w-5 transition-transform"
        :class="collapsed && 'rotate-180'"
      />
    </button>
  </aside>
</template>