import type { MaybeElementRef } from '@vueuse/core'
import type { Ref, WatchSource } from 'vue'
import { nextTick, unref, watch } from 'vue'

export function useAutoScroll(containerRef: MaybeElementRef<HTMLElement | null>) {
  const scrollToBottom = async () => {
    const container = unref(containerRef)
    await nextTick()
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  }

  const setupAutoScroll = <T>(watchSource: WatchSource<T> | Ref<T>) => {
    watch(watchSource, scrollToBottom, { deep: true })
  }

  return {
    setupAutoScroll,
  }
}
