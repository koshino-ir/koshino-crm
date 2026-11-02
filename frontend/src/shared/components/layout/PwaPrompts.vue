<script setup lang="ts">
import { Download, RefreshCw, WifiOff, X } from "lucide-vue-next"
import { ref } from "vue"

import { usePwa } from "@/core/pwa/usePwa"
import { Button } from "@/shared/components/ui/button"

const { canInstall, isOffline, updateAvailable, install, applyUpdate, dismissUpdate } =
  usePwa()

const installDismissed = ref(false)

async function onInstall() {
  const accepted = await install()
  if (!accepted) installDismissed.value = true
}
</script>

<template>
  <!-- Offline banner -->
  <Transition
    enter-active-class="transition duration-200"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-150"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="isOffline"
      class="fixed bottom-0 inset-x-0 z-50 flex items-center justify-center gap-2 bg-amber-500 px-4 py-2 text-sm font-medium text-white shadow-lg"
    >
      <WifiOff class="h-4 w-4" />
      {{ $t("pwa.offline") }}
    </div>
  </Transition>

  <!-- Update available banner -->
  <Transition
    enter-active-class="transition duration-200"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-150"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="updateAvailable"
      class="fixed bottom-4 end-4 z-50 flex max-w-sm items-start gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-xl dark:border-slate-700 dark:bg-slate-900"
    >
      <RefreshCw class="h-5 w-5 shrink-0 text-primary-600" />
      <div class="min-w-0 flex-1">
        <div class="font-medium text-slate-900 dark:text-slate-100">
          {{ $t("pwa.update_title") }}
        </div>
        <p class="mt-0.5 text-sm text-slate-500">{{ $t("pwa.update_message") }}</p>
        <div class="mt-3 flex gap-2">
          <Button size="sm" @click="applyUpdate">{{ $t("pwa.reload") }}</Button>
          <Button size="sm" variant="ghost" @click="dismissUpdate">
            {{ $t("pwa.later") }}
          </Button>
        </div>
      </div>
      <button
        class="rounded p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
        @click="dismissUpdate"
      >
        <X class="h-4 w-4" />
      </button>
    </div>
  </Transition>

  <!-- Install prompt -->
  <Transition
    enter-active-class="transition duration-200"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-150"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="canInstall && !installDismissed && !isOffline"
      class="fixed bottom-4 start-4 z-50 flex max-w-sm items-start gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-xl dark:border-slate-700 dark:bg-slate-900"
    >
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary-600 font-bold text-white">
        K
      </div>
      <div class="min-w-0 flex-1">
        <div class="font-medium text-slate-900 dark:text-slate-100">
          {{ $t("pwa.install_title") }}
        </div>
        <p class="mt-0.5 text-sm text-slate-500">{{ $t("pwa.install_message") }}</p>
        <div class="mt-3 flex gap-2">
          <Button size="sm" @click="onInstall">
            <Download class="h-3.5 w-3.5" />
            {{ $t("pwa.install_button") }}
          </Button>
          <Button size="sm" variant="ghost" @click="installDismissed = true">
            {{ $t("pwa.later") }}
          </Button>
        </div>
      </div>
      <button
        class="rounded p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
        @click="installDismissed = true"
      >
        <X class="h-4 w-4" />
      </button>
    </div>
  </Transition>
</template>