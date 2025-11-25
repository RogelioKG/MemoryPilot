<script setup lang="ts">
import type { FileTypes } from '../../types'
import { useDropZone } from '@vueuse/core'
import { useTemplateRef, watch } from 'vue'
import StarryNight from '../../components/background/StarryNight.vue'

// props //
const props = defineProps<{
  dataTypes?: FileTypes
}>()

// emit //
// 檔案上傳事件
const emit = defineEmits<{
  (e: 'upload', files: File[]): void
}>()
// template ref //
const dropZoneRef = useTemplateRef('dropZoneRef')
const starryNightRef = useTemplateRef('starryNightRef')

// methods //
function onDrop(files: File[] | null) {
  if (files) {
    emit('upload', files)
  }
}

// composables //
const { isOverDropZone } = useDropZone(dropZoneRef, {
  dataTypes: props.dataTypes,
  onDrop,
})

// watch //
watch(isOverDropZone, () => {
  if (isOverDropZone.value) {
    starryNightRef.value?.enableStarryEffect()
  }
  else {
    starryNightRef.value?.disableStarryEffect()
  }
})
</script>

<template>
  <div ref="dropZoneRef" class="drop-zone">
    <div class="drop-zone-content" :class="{ fade: isOverDropZone }">
      <slot />
    </div>
    <StarryNight ref="starryNightRef" />
  </div>
</template>

<style scoped lang="css">
.drop-zone {
  position: relative;
  width: 100%;
  height: 100%;
}

.drop-zone-content {
  position: absolute;
  width: 100%;
  top: 20%;
  font-size: 1.3rem;
  text-align: center;
  z-index: 1;
  opacity: 0.4;
  transition: opacity 1.5s ease-out;
}

.fade {
  opacity: 0;
}
</style>
