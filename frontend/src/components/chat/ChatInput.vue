<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { nextTick, ref, useTemplateRef, watch } from 'vue'
import UploadButton from '../button/UploadButton.vue'
import SendIcon from '../icon/SendIcon.vue'

// emit //
const emit = defineEmits<{
  (e: 'send', payload: { message: string, files?: File[] }): void
}>()

// template ref //
const textarea = useTemplateRef<HTMLTextAreaElement>('textarea')

// ref //
const newMessage = ref('')
const fileArea = ref<File[]>([])

// methods //
function handleKeydown(e: KeyboardEvent) {
  if (e.key !== 'Enter')
    return
  if (e.shiftKey)
    return // Shift + Enter 新行
  e.preventDefault()
  sendMessage() // Enter 送出
}

async function adjustTextareaHeight(minHeight: number, maxHeight: number) {
  await nextTick()
  const el = textarea.value
  if (!el)
    return

  el.style.height = 'auto' // 重算高度 (以免被撐高後 scrollHeight 回不去)
  el.style.height = `${Math.min(Math.max(el.scrollHeight, minHeight), maxHeight)}px`
}

function appendFiles(files: File[]) {
  fileArea.value.push(...files)
}

function removeFile(i: number) {
  fileArea.value.splice(i, 1)
}

function sendMessage() {
  if (!newMessage.value.trim() && !fileArea.value.length)
    return

  emit('send', {
    message: newMessage.value,
    files: [...fileArea.value],
  })

  newMessage.value = ''
  fileArea.value = []
  if (textarea.value) {
    textarea.value.style.height = 'auto' // 重算高度
  }
}

// watch //
watch(newMessage, () => {
  adjustTextareaHeight(45, 150)
})
</script>

<template>
  <div class="chat-input">
    <div v-if="fileArea.length" class="file-row">
      <div v-for="(file, i) in fileArea" :key="`${file.name}-${i}`" class="file-item">
        <span class="file-name">{{ file.name }}</span>
        <button class="remove-button" type="button" @click="removeFile(i)">
          <Icon icon="material-symbols:close" width="20" height="20" style="color: var(--primary-color)" />
        </button>
      </div>
    </div>
    <div class="input-row">
      <UploadButton @upload="appendFiles" />
      <textarea
        ref="textarea" v-model="newMessage" placeholder="問我酷問題..." rows="1" class="input-area"
        @keydown="handleKeydown"
      />
      <button :disabled="!newMessage.trim() && !fileArea.length" class="send-button" @click="sendMessage">
        <SendIcon />
      </button>
    </div>
  </div>
</template>

<style scoped lang="css">
.chat-input {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg);
  gap: var(--spacing-md);
  background-color: var(--secondary-color);
  border-top: 1px solid var(--primary-color-brighter);
}

.input-row {
  flex: 1;
  align-items: flex-start;
  display: flex;
  flex-direction: row;
  gap: var(--spacing-sm);
}

.input-area {
  flex: 1;
  font-family: inherit;
  font-size: 1.1em;
  font-weight: 300;
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--primary-color);
  background-color: var(--input-unfocused);
  border: 1px solid var(--primary-color-bright);
  border-radius: var(--border-radius-sm);
  resize: none;
  min-height: 45px;
  max-height: 150px;
  overflow-y: auto;
  vertical-align: bottom;
  transition:
    height 0.2s ease,
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.input-area::placeholder {
  color: var(--placeholder-color);
}

.input-area:focus {
  outline: none;
  background-color: var(--input-focused);
  border-color: var(--primary-active-color);
}

.send-button {
  font-family: inherit;
  height: 45px;
  padding: 0 var(--spacing-lg);
  color: var(--primary-color);
  background-color: var(--primary-color-dim);
  border: 1px solid var(--primary-color-bright);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:disabled {
  color: var(--primary-color-bright);
  border-color: var(--primary-color-dim);
  background-color: var(--primary-color-shadowy);
  cursor: not-allowed;
}

.send-button:hover:not(:disabled) {
  border-color: var(--primary-active-color);
  background-color: var(--primary-active-color-bright);
}

.file-row {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.file-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 8px 10px;
  background: var(--gray-color-bright);
  border: 1px solid var(--primary-color-dim);
  border-radius: 8px;
}

.file-name {
  max-width: 150px;
  font-size: 0.8em;
  color: var(--primary-color);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-button {
  display: flex;
  background: transparent;
  border: none;
  cursor: pointer;
}
</style>
