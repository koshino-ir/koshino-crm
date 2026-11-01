<script setup lang="ts">
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"

import { ApiError } from "@/core/api/client"
import { useAuthStore } from "@/core/stores/auth"
import { Button } from "@/shared/components/ui/button"
import { Card } from "@/shared/components/ui/card"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { AuthLayout } from "@/shared/layouts"

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()

const form = ref({
  email: "",
  password: "",
  confirm_password: "",
  first_name: "",
  last_name: "",
  organization_name: "",
})

const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

function clearErrors() {
  generalError.value = ""
  fieldErrors.value = {}
}

function firstFieldError(field: string): string | null {
  const list = fieldErrors.value[field]
  return list && list.length > 0 ? list[0] : null
}

async function submit() {
  clearErrors()

  if (form.value.password !== form.value.confirm_password) {
    fieldErrors.value.confirm_password = ["Passwords do not match"]
    return
  }

  try {
    await auth.register({
      email: form.value.email,
      password: form.value.password,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      organization_name: form.value.organization_name,
    })
    router.replace("/dashboard")
  } catch (err) {
    if (err instanceof ApiError) {
      const fields = err.fieldErrors()
      fieldErrors.value = fields

      // If there are only non-field errors (or none), show a summary banner
      const hasFieldErrors = Object.keys(fields).some(
        (k) => k !== "non_field_errors" && k !== "detail",
      )
      if (!hasFieldErrors) {
        generalError.value =
          fields.non_field_errors?.[0] ?? err.firstError()
      }
    } else {
      generalError.value = err instanceof Error ? err.message : t("common.error")
    }
  }
}
</script>

<template>
  <AuthLayout>
    <Card class="p-6">
      <div class="mb-6 space-y-1">
        <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100">
          {{ $t("auth.register_title") }}
        </h2>
        <p class="text-sm text-slate-500">{{ $t("auth.register_subtitle") }}</p>
      </div>

      <form class="space-y-4" novalidate @submit.prevent="submit">
        <div class="grid grid-cols-2 gap-3">
          <div class="space-y-1">
            <label class="text-sm font-medium" for="fn">{{ $t("auth.first_name") }}</label>
            <Input
              id="fn"
              v-model="form.first_name"
              autocomplete="given-name"
              :class="firstFieldError('first_name') && 'border-rose-500'"
            />
            <p v-if="firstFieldError('first_name')" class="text-xs text-rose-600">
              {{ firstFieldError("first_name") }}
            </p>
          </div>
          <div class="space-y-1">
            <label class="text-sm font-medium" for="ln">{{ $t("auth.last_name") }}</label>
            <Input
              id="ln"
              v-model="form.last_name"
              autocomplete="family-name"
              :class="firstFieldError('last_name') && 'border-rose-500'"
            />
            <p v-if="firstFieldError('last_name')" class="text-xs text-rose-600">
              {{ firstFieldError("last_name") }}
            </p>
          </div>
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium" for="org">{{ $t("auth.org_name") }}</label>
          <Input
            id="org"
            v-model="form.organization_name"
            required
            :class="firstFieldError('organization_name') && 'border-rose-500'"
          />
          <p v-if="firstFieldError('organization_name')" class="text-xs text-rose-600">
            {{ firstFieldError("organization_name") }}
          </p>
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium" for="email">{{ $t("auth.email") }}</label>
          <Input
            id="email"
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            :class="firstFieldError('email') && 'border-rose-500'"
          />
          <p v-if="firstFieldError('email')" class="text-xs text-rose-600">
            {{ firstFieldError("email") }}
          </p>
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium" for="pw">{{ $t("auth.password") }}</label>
          <Input
            id="pw"
            v-model="form.password"
            type="password"
            autocomplete="new-password"
            required
            :class="firstFieldError('password') && 'border-rose-500'"
          />
          <p v-if="firstFieldError('password')" class="text-xs text-rose-600">
            {{ firstFieldError("password") }}
          </p>
        </div>

        <div class="space-y-1">
          <label class="text-sm font-medium" for="cpw">{{ $t("auth.confirm_password") }}</label>
          <Input
            id="cpw"
            v-model="form.confirm_password"
            type="password"
            autocomplete="new-password"
            required
            :class="firstFieldError('confirm_password') && 'border-rose-500'"
          />
          <p v-if="firstFieldError('confirm_password')" class="text-xs text-rose-600">
            {{ firstFieldError("confirm_password") }}
          </p>
        </div>

        <p
          v-if="generalError"
          class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
        >
          {{ generalError }}
        </p>

        <Button type="submit" class="w-full" :disabled="auth.loading">
          <Spinner v-if="auth.loading" size="sm" />
          <span v-else>{{ $t("auth.register") }}</span>
        </Button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-500">
        {{ $t("auth.have_account") }}
        <RouterLink :to="{ name: 'login' }" class="font-medium text-primary-600 hover:underline">
          {{ $t("auth.login") }}
        </RouterLink>
      </p>
    </Card>
  </AuthLayout>
</template>