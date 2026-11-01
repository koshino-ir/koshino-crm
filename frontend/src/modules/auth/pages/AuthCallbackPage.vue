<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { Spinner } from "@/shared/components/ui/spinner"

const route = useRoute()
const router = useRouter()
const error = ref("")

onMounted(() => {
  if (route.query.error) {
    error.value = String(route.query.error)
    setTimeout(() => router.replace({ name: "login" }), 2000)
    return
  }
  // A full reload guarantees the browser has applied the new cookies
  // and the auth store re-initializes from /auth/me with fresh session.
  window.location.replace("/dashboard")
})
</script>

<template>
  <div class="flex min-h-screen items-center justify-center">
    <div v-if="error" class="text-rose-600 text-sm">Error: {{ error }}</div>
    <div v-else class="flex items-center gap-2 text-slate-500">
      <Spinner />
      <span>Completing sign-in…</span>
    </div>
  </div>
</template>