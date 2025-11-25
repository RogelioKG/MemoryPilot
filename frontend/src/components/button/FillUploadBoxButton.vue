<script setup lang="ts">
import type { FileTypes } from '../../types'
import { extractFiles } from '../../utils/misc/file'
import PosBoxButton from './PosBoxButton.vue'

// props //
const props = defineProps<{
  dataTypes?: FileTypes
}>()

// emit //
const emit = defineEmits<{
  (e: 'upload', file: File[]): void // 檔案上傳事件
}>()

// methods //
function handleChange(event: Event) {
  emit('upload', extractFiles(event, props.dataTypes))
}
</script>

<template>
  <PosBoxButton tag="label" for="file-uploader">
    <input id="file-uploader" type="file" multiple @change="handleChange">
    <slot />
  </PosBoxButton>
</template>

<style scoped lang="css">
#file-uploader {
  display: none;
}
</style>
