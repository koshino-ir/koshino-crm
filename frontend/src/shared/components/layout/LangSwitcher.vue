<script setup lang="ts">
import { ChevronDown, Globe } from "lucide-vue-next"
import { computed, onBeforeUnmount, onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"

import { setLocale, type AppLocale } from "@/core/i18n"

const { locale } = useI18n()
const open = ref(false)
const root = ref<HTMLElement | null>(null)

const LANGUAGES: Array<{ code: AppLocale; label: string; native: string }> = [
  { code: "fa", label: "Persian", native: "فارسی" },
  { code: "en", label: "English", native: "English" },
  { code: "ar", label: "Arabic", native: "العربية" },
]

const current = computed(
  () => LANGUAGES.find((l) => l.code === locale.value) ?? LANGUAGES[0],
)

function choose(code: AppLocale) {
  setLocale(code)
  open.value = false
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
      class="inline-flex h-9 items-center gap-2 rounded-md px-2 text-sm text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
      @click="open = !open"
    >
      <Globe class="h-4 w-4" />
      <span class="hidden sm:inline">{{ current.native }}</span>
      <ChevronDown class="h-3.5 w-3.5" />
    </button>
    <div
      v-if="open"
      class="absolute end-0 z-50 mt-1 w-40 rounded-md border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-700 dark:bg-slate-900"
    >
      <button
        v-for="lang in LANGUAGES"
        :key="lang.code"
        class="block w-full px-3 py-2 text-start text-sm hover:bg-slate-50 dark:hover:bg-slate-800"
        :class="{
          'bg-slate-100 font-medium dark:bg-slate-800': lang.code === locale,
        }"
        @click="choose(lang.code)"
      >
        <div class="flex items-center justify-between">
          <span>{{ lang.native }}</span>
          <span class="text-xs text-slate-500">{{ lang.label }}</span>
        </div>
      </button>
    </div>
  </div>
</template>