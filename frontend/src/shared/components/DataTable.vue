<script setup lang="ts" generic="T extends { id: string | number }">
import { Skeleton } from "@/shared/components/ui/skeleton"

export interface Column {
  key: string
  label: string
  align?: "start" | "center" | "end"
  thClass?: string
  tdClass?: string
}

interface Props {
  columns: Column[]
  rows: T[]
  loading?: boolean
  emptyMessage?: string
}

withDefaults(defineProps<Props>(), {
  loading: false,
  emptyMessage: "No results",
})

const alignClass = (a?: Column["align"]) =>
  a === "center" ? "text-center" : a === "end" ? "text-end" : "text-start"
</script>

<template>
  <div class="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-800">
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-slate-50 dark:bg-slate-900">
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-4 py-3 font-medium text-slate-600 dark:text-slate-400',
                alignClass(col.align),
                col.thClass,
              ]"
            >
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
          <tr v-if="loading">
            <td :colspan="columns.length" class="p-4">
              <Skeleton v-for="i in 5" :key="i" class="mb-2 h-8 w-full" />
            </td>
          </tr>

          <tr v-else-if="rows.length === 0">
            <td :colspan="columns.length" class="px-4 py-12 text-center text-slate-500">
              {{ emptyMessage }}
            </td>
          </tr>

          <tr
            v-else
            v-for="row in rows"
            :key="String(row.id)"
            class="bg-white hover:bg-slate-50 dark:bg-slate-900 dark:hover:bg-slate-800/60"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              :class="['px-4 py-3', alignClass(col.align), col.tdClass]"
            >
              <slot :name="`cell:${col.key}`" :row="row">
                {{ (row as Record<string, unknown>)[col.key] ?? "—" }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>