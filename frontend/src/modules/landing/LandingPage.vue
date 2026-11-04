<script setup lang="ts">
import {
  ArrowRight,
  BarChart3,
  Building2,
  CheckCircle2,
  Globe,
  Kanban,
  Shield,
  Users,
  Zap,
} from "lucide-vue-next"
import type { Component } from "vue"
import { computed } from "vue"
import { useI18n } from "vue-i18n"

import { useSeo } from "@/core/seo/useSeo"
import { LangSwitcher, ThemeToggle } from "@/shared/components/layout"
import { Button } from "@/shared/components/ui/button"

const { t } = useI18n()

useSeo({
  title: t("landing.meta_title"),
  description: t("landing.meta_description"),
  url: "/",
})

interface Feature {
  icon: Component
  title: string
  body: string
}

const features = computed<Feature[]>(() => [
  {
    icon: Kanban,
    title: t("landing.features.pipeline.title"),
    body: t("landing.features.pipeline.body"),
  },
  {
    icon: Building2,
    title: t("landing.features.companies.title"),
    body: t("landing.features.companies.body"),
  },
  {
    icon: Users,
    title: t("landing.features.contacts.title"),
    body: t("landing.features.contacts.body"),
  },
  {
    icon: BarChart3,
    title: t("landing.features.dashboard.title"),
    body: t("landing.features.dashboard.body"),
  },
  {
    icon: Globe,
    title: t("landing.features.multilang.title"),
    body: t("landing.features.multilang.body"),
  },
  {
    icon: Shield,
    title: t("landing.features.security.title"),
    body: t("landing.features.security.body"),
  },
])

// Structured data for Google
const jsonLd = computed(() => ({
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Koshino CRM",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  description: t("landing.meta_description"),
  offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
}))
</script>

<template>
  <!-- JSON-LD -->
  <component :is="'script'" type="application/ld+json">
    {{ JSON.stringify(jsonLd) }}
  </component>

  <div class="min-h-screen bg-white dark:bg-slate-950">
    <!-- Header -->
    <header class="border-b border-slate-200 dark:border-slate-800">
      <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <div class="flex items-center gap-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-md bg-primary-600 font-bold text-white">
            K
          </div>
          <span class="text-lg font-semibold text-slate-900 dark:text-slate-100">Koshino</span>
        </div>
        <div class="flex items-center gap-2">
          <LangSwitcher />
          <ThemeToggle />
          <RouterLink :to="{ name: 'login' }">
            <Button variant="ghost">{{ $t("landing.sign_in") }}</Button>
          </RouterLink>
          <RouterLink :to="{ name: 'register' }" class="hidden sm:inline-block">
            <Button>{{ $t("landing.get_started") }}</Button>
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative overflow-hidden">
      <div class="absolute inset-0 -z-10 bg-gradient-to-b from-primary-50/60 to-white dark:from-primary-950/20 dark:to-slate-950" />
      <div class="mx-auto max-w-4xl px-4 py-24 text-center">
        <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-primary-200 bg-primary-50 px-3 py-1 text-xs font-medium text-primary-700 dark:border-primary-800 dark:bg-primary-950/60 dark:text-primary-300">
          <Zap class="h-3 w-3" />
          {{ $t("landing.badge") }}
        </div>
        <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl md:text-6xl dark:text-slate-100">
          {{ $t("landing.hero_title") }}
        </h1>
        <p class="mx-auto mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
          {{ $t("landing.hero_subtitle") }}
        </p>
        <div class="mt-8 flex flex-wrap items-center justify-center gap-3">
          <RouterLink :to="{ name: 'register' }">
            <Button size="lg">
              {{ $t("landing.cta_primary") }}
              <ArrowRight class="h-4 w-4 rtl:rotate-180" />
            </Button>
          </RouterLink>
          <RouterLink :to="{ name: 'login' }">
            <Button size="lg" variant="outline">{{ $t("landing.cta_secondary") }}</Button>
          </RouterLink>
        </div>
        <div class="mt-6 flex flex-wrap items-center justify-center gap-4 text-sm text-slate-500">
          <span class="flex items-center gap-1.5">
            <CheckCircle2 class="h-4 w-4 text-emerald-500" />
            {{ $t("landing.trust.no_credit") }}
          </span>
          <span class="flex items-center gap-1.5">
            <CheckCircle2 class="h-4 w-4 text-emerald-500" />
            {{ $t("landing.trust.setup") }}
          </span>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="border-t border-slate-100 py-20 dark:border-slate-800">
      <div class="mx-auto max-w-6xl px-4">
        <div class="mx-auto mb-12 max-w-2xl text-center">
          <h2 class="text-3xl font-bold text-slate-900 dark:text-slate-100">
            {{ $t("landing.features_title") }}
          </h2>
          <p class="mt-3 text-slate-600 dark:text-slate-400">
            {{ $t("landing.features_subtitle") }}
          </p>
        </div>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="f in features"
            :key="f.title"
            class="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900"
          >
            <div class="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-md bg-primary-100 text-primary-600 dark:bg-primary-950/60 dark:text-primary-400">
              <component :is="f.icon" class="h-5 w-5" />
            </div>
            <h3 class="mb-1.5 font-semibold text-slate-900 dark:text-slate-100">{{ f.title }}</h3>
            <p class="text-sm leading-relaxed text-slate-600 dark:text-slate-400">{{ f.body }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="border-t border-slate-100 bg-gradient-to-b from-primary-50 to-white py-20 dark:border-slate-800 dark:from-primary-950/20 dark:to-slate-950">
      <div class="mx-auto max-w-2xl px-4 text-center">
        <h2 class="text-3xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("landing.cta_title") }}
        </h2>
        <p class="mt-3 text-slate-600 dark:text-slate-400">{{ $t("landing.cta_subtitle") }}</p>
        <div class="mt-8">
          <RouterLink :to="{ name: 'register' }">
            <Button size="lg">
              {{ $t("landing.cta_primary") }}
              <ArrowRight class="h-4 w-4 rtl:rotate-180" />
            </Button>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-slate-100 py-8 dark:border-slate-800">
      <div class="mx-auto max-w-6xl px-4">
        <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div class="text-sm text-slate-500">
            © {{ new Date().getFullYear() }} Koshino. {{ $t("landing.rights") }}
          </div>
          <div class="flex items-center gap-4 text-sm">
            <RouterLink :to="{ name: 'login' }" class="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
              {{ $t("landing.sign_in") }}
            </RouterLink>
            <RouterLink :to="{ name: 'register' }" class="text-primary-600 hover:underline">
              {{ $t("landing.get_started") }}
            </RouterLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>