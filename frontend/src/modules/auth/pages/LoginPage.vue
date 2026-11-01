<script setup lang="ts">
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute, useRouter } from "vue-router"

import { ApiError } from "@/core/api/client"
import { authApi } from "@/core/api/endpoints/auth"
import { useAuthStore } from "@/core/stores/auth"
import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { AuthLayout } from "@/shared/layouts"

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref("")
const password = ref("")
const errorMessage = ref("")

async function submit() {
  errorMessage.value = ""
  try {
    await auth.login({ email: email.value, password: password.value })
    const redirect = (route.query.redirect as string) || "/dashboard"
    router.replace(redirect)
  } catch (err) {
    // Prefer field-level / specific message
    errorMessage.value =
      err instanceof ApiError
        ? err.firstError()
        : err instanceof Error
          ? err.message
          : t("common.error")
  }
}

async function googleLogin() {
  try {
    const url = await authApi.googleUrl(window.location.origin + "/auth/callback")
    window.location.href = url
  } catch (err) {
    errorMessage.value =
      err instanceof ApiError ? err.firstError() : t("common.error")
  }
}
</script>

<template>
  <AuthLayout>
    <Card class="p-6">
      <div class="mb-6 space-y-1">
        <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("auth.welcome") }}
        </h2>
        <p class="text-sm text-slate-500">{{ $t("auth.subtitle") }}</p>
      </div>

      <form class="space-y-4" @submit.prevent="submit">
        <div class="space-y-1">
          <label class="text-sm font-medium" for="email">{{ $t("auth.email") }}</label>
          <Input
            id="email"
            v-model="email"
            type="email"
            autocomplete="email"
            required
            placeholder="you@example.com"
          />
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium" for="password">{{ $t("auth.password") }}</label>
          <Input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
            placeholder="••••••••"
          />
        </div>

        <p
          v-if="errorMessage"
          class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
        >
          {{ errorMessage }}
        </p>

        <Button type="submit" class="w-full" :disabled="auth.loading">
          <Spinner v-if="auth.loading" size="sm" />
          <span v-else>{{ $t("auth.login") }}</span>
        </Button>
      </form>

      <div class="my-4 flex items-center gap-3">
        <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
        <span class="text-xs text-slate-500">{{ $t("auth.or") }}</span>
        <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
      </div>

      <Button variant="outline" class="w-full" type="button" @click="googleLogin">
        {{ $t("auth.google_login") }}
      </Button>

      <p class="mt-6 text-center text-sm text-slate-500">
        {{ $t("auth.no_account") }}
        <RouterLink :to="{ name: 'register' }" class="font-medium text-primary-600 hover:underline">
          {{ $t("auth.register") }}
        </RouterLink>
      </p>
    </Card>
  </AuthLayout>
</template>