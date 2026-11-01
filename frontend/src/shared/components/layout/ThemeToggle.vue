<script setup lang="ts">
import { Moon, Sun } from "lucide-vue-next"

import { useUiStore } from "@/core/stores/ui"

const ui = useUiStore()
</script>

<template>
  <button
    type="button"
    class="inline-flex h-9 w-9 items-center justify-center rounded-md text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
    :aria-label="ui.isDark ? $t('layout.light') : $t('layout.dark')"
    @click="ui.toggleTheme()"
  >
    <Sun v-if="ui.isDark" class="h-5 w-5" />
    <Moon v-else class="h-5 w-5" />
  </button>
</template>