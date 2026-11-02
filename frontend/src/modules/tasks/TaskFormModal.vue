<script setup lang="ts">
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { computed, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import { ApiError } from "@/core/api/client"
import { FormModal } from "@/shared/components"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Select } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { Textarea } from "@/shared/components/ui/textarea"

import { taskKeys, tasksApi } from "./api"
import type { Task, TaskPriority, TaskStatus, TaskWritePayload } from "./types"

interface Props {
  open: boolean
  editing: Task | null
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: []; saved: [] }>()
const { t } = useI18n()
const queryClient = useQueryClient()

const empty = (): TaskWritePayload => ({
  title: "",
  description: "",
  due_date: null,
  priority: "medium",
  status: "todo",
})

const form = ref<TaskWritePayload>(empty())
const generalError = ref("")
const fieldErrors = ref<Record<string, string[]>>({})

watch(
  () => props.editing,
  (c) => {
    fieldErrors.value = {}
    generalError.value = ""
    form.value = c
      ? {
          title: c.title,
          description: c.description,
          due_date: c.due_date,
          priority: c.priority,
          status: c.status,
        }
      : empty()
  },
  { immediate: true },
)

const priorityOptions = computed(() => [
  { value: "low", label: t("tasks.priorities.low") },
  { value: "medium", label: t("tasks.priorities.medium") },
  { value: "high", label: t("tasks.priorities.high") },
  { value: "urgent", label: t("tasks.priorities.urgent") },
])

const statusOptions = computed(() => [
  { value: "todo", label: t("tasks.statuses.todo") },
  { value: "in_progress", label: t("tasks.statuses.in_progress") },
  { value: "done", label: t("tasks.statuses.done") },
])

const { mutate: save, isPending } = useMutation({
  mutationFn: () =>
    props.editing
      ? tasksApi.update(props.editing.id, form.value)
      : tasksApi.create(form.value),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: taskKeys.all })
    emit("saved")
  },
  onError: (err) => {
    if (err instanceof ApiError) {
      fieldErrors.value = err.fieldErrors()
      generalError.value = err.firstError()
    }
  },
})

function submit() {
  generalError.value = ""
  fieldErrors.value = {}
  if (!form.value.title.trim()) {
    fieldErrors.value.title = [t("tasks.form.title_required")]
    return
  }
  save()
}

const err = (k: string) => fieldErrors.value[k]?.[0] ?? null
</script>

<template>
  <FormModal
    :open="props.open"
    :title="props.editing ? $t('tasks.edit_title') : $t('tasks.new')"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <div>
        <label class="text-sm font-medium">{{ $t("tasks.form.title") }} *</label>
        <Input v-model="form.title" :class="err('title') && 'border-rose-500'" />
        <p v-if="err('title')" class="text-xs text-rose-600">{{ err("title") }}</p>
      </div>

      <div>
        <label class="text-sm font-medium">{{ $t("tasks.form.description") }}</label>
        <Textarea v-model="form.description" :rows="3" />
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div>
          <label class="text-sm font-medium">{{ $t("tasks.form.due") }}</label>
          <Input v-model="form.due_date as string" type="date" />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("tasks.form.priority") }}</label>
          <Select
            :model-value="form.priority ?? 'medium'"
            :options="priorityOptions"
            @update:model-value="(v) => (form.priority = (v ?? 'medium') as TaskPriority)"
          />
        </div>
        <div>
          <label class="text-sm font-medium">{{ $t("tasks.form.status") }}</label>
          <Select
            :model-value="form.status ?? 'todo'"
            :options="statusOptions"
            @update:model-value="(v) => (form.status = (v ?? 'todo') as TaskStatus)"
          />
        </div>
      </div>

      <p
        v-if="generalError"
        class="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
      >
        {{ generalError }}
      </p>
    </div>

    <template #actions>
      <Button variant="outline" @click="emit('close')">{{ $t("common.cancel") }}</Button>
      <Button :disabled="isPending" @click="submit">
        <Spinner v-if="isPending" size="sm" />
        <span v-else>{{ $t("common.save") }}</span>
      </Button>
    </template>
  </FormModal>
</template>