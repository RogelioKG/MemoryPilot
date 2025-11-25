<script setup lang="ts">
import type { FileTypes } from '../../types'
import { useTemplateRef } from 'vue'
import { extractFiles } from '../../utils/misc/file'
import { isTouchDevice } from '../../utils/misc/methods'
import UploadIcon from '../icon/UploadIcon.vue'
import FileUploadModal from '../modal/FileUploadModal.vue'

// props //
const props = defineProps<{
  dataTypes?: FileTypes
}>()

// emit //
const emit = defineEmits<{
  (e: 'upload', files: File[]): void
}>()

// template ref //
const fileInput = useTemplateRef('fileInput')
const modalDropRef = useTemplateRef('modalDropRef')

// methods //
function handleClick() {
  if (isTouchDevice) {
    // 手機不顯示 modal
    fileInput.value?.click()
  }
  else {
    // 桌機顯示 modal
    modalDropRef.value?.showModal()
  }
}

function handleChange(event: Event) {
  const files = extractFiles(event, props.dataTypes)
  emit('upload', files)
}

function handleFileUpload(files: File[]) {
  emit('upload', files)
}
</script>

<template>
  <div class="file-upload">
    <input ref="fileInput" type="file" class="hidden-input" @change="handleChange">
    <button type="button" class="upload-button" title="Upload file" @click="handleClick">
      <UploadIcon />
    </button>
  </div>
  <Teleport to="body">
    <FileUploadModal ref="modalDropRef" @upload="handleFileUpload" />
  </Teleport>
</template>

<style scoped lang="css">
.file-upload {
  position: relative;
}

.hidden-input {
  display: none;
}

.upload-button {
  height: 45px;
  width: 45px;
  color: var(--primary-color);
  border: 1px solid var(--primary-color-bright);
  background-color: var(--primary-color-dim);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button:hover {
  border-color: var(--primary-active-color);
  background-color: var(--primary-active-color-bright);
}

.upload-button svg {
  transition: transform 0.2s ease;
}

.upload-button:hover svg {
  transform: scale(1.1);
}
</style>
