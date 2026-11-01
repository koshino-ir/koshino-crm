import { ref, watch, type Ref } from "vue"

export function useDebouncedRef<T>(source: Ref<T>, delay = 300): Ref<T> {
    const debounced = ref(source.value) as Ref<T>
    let timer: ReturnType<typeof setTimeout> | null = null
    watch(source, (v) => {
        if (timer) clearTimeout(timer)
        timer = setTimeout(() => {
            debounced.value = v
        }, delay)
    })
    return debounced
}