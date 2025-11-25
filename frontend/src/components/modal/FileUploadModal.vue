<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useTemplateRef } from 'vue'
import DropZone from '../../components/misc/DropZone.vue'
import BoxButton from '../button/BoxButton.vue'
import FillUploadBoxButton from '../button/FillUploadBoxButton.vue'
import BaseModal from './BaseModal.vue'

// emit //
const emit = defineEmits<{
  (e: 'upload', file: File[]): void
}>()

// template ref //
const baseModalRef = useTemplateRef('baseModalRef')

// methods //
function handleFileUpload(files: File[]) {
  emit('upload', files)
  baseModalRef.value?.closeModal()
}

// expose //
defineExpose({
  isShow: () => baseModalRef.value?.isShow(),
  showModal: () => baseModalRef.value?.showModal(),
  closeModal: () => baseModalRef.value?.closeModal(),
})
</script>

<template>
  <BaseModal ref="baseModalRef">
    <template #header>
      <div class="modal-header">
        <div class="close-btn-block">
          <BoxButton tag="button" class="close-btn rounded" @click="baseModalRef?.closeModal()">
            <Icon icon="material-symbols:close" width="20" height="20" style="color: var(--primary-color)" />
          </BoxButton>
        </div>
      </div>
    </template>
    <template #body>
      <div class="modal-body">
        <div class="drop-block">
          <DropZone @upload="handleFileUpload">
            Drop files here...
          </DropZone>
        </div>
        <div class="upload-block">
          <div class="upload-block-content">
            or
          </div>
          <FillUploadBoxButton @upload="handleFileUpload">
            Choose File
          </FillUploadBoxButton>
        </div>
      </div>
    </template>
  </BaseModal>
</template>

<style scoped lang="css">
.modal-body {
  font-weight: 500;
  color: var(--primary-color);
  background-color: black;
  width: 500px;
  height: 600px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--primary-color-shadowy);
}

.drop-block {
  width: 100%;
  height: 300px;
}

.upload-block {
  width: 100%;
  height: 300px;
  display: flex;
  flex-flow: column;
  justify-content: start;
  align-items: center;
}

.upload-block-content {
  display: flex;
  align-items: center;
  height: 40%;
}

.close-btn-block {
  position: absolute;
  top: -10px;
  right: -10px;
  z-index: 1;
}

.close-btn {
  color: var(--primary-color);
  background-color: var(--gray-color);
  border: 1px solid var(--primary-color-shadowy);
}

.rounded {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
</style>
