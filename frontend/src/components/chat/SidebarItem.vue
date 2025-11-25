<script setup lang="ts">
import type { Conversation } from '../../types'
import { Icon } from '@iconify/vue'

// props //
defineProps<{
  conversation: Conversation
  isActive: boolean
  isOpen: boolean
  index: number
}>()

// emit //
const emit = defineEmits<{
  (e: 'select'): void
  (e: 'delete'): void
}>()

// methods //
function getPreviewText(conversation: Conversation): string {
  const lastMessage = conversation.messages[conversation.messages.length - 1]
  return lastMessage ? lastMessage.text : 'No messages'
}

function handleDelete() {
  if (confirm('Are you sure you want to delete this chat?')) {
    emit('delete')
  }
}
</script>

<template>
  <div
    class="history-item"
    :class="{
      'active': isActive,
      'slide-in': isOpen,
    }"
    :style="{
      '--delay': `${index * 0.05}s`,
      '--distance': `${(index + 1) * 10}px`,
    }"
  >
    <div class="history-item-content" @click="emit('select')">
      <div class="history-item-header">
        <span class="history-title">{{ conversation.title }}</span>
      </div>
      <p class="history-preview">
        {{ getPreviewText(conversation) }}
      </p>
    </div>
    <button class="delete-button" @click.stop="handleDelete">
      <Icon icon="material-symbols:close" width="20" height="20" style="color: var(--primary-color)" />
    </button>
  </div>
</template>

<style scoped lang="css">
.history-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--primary-color-dim);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  transition: all 0.2s ease;
  cursor: pointer;
  display: flex;
  align-items: stretch;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.history-item.active {
  background: var(--primary-color-shadowy);
  border-color: var(--primary-color-brighter);
}

.history-item-content {
  flex: 1;
  /* 讓 history-preview 能跟著父元素寬度動態 text-overflow: ellipsis */
  min-width: 0;
  padding: var(--spacing-md);
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.history-title {
  font-weight: 600;
  font-size: 1.1em;
  color: var(--primary-color);
}

.history-preview {
  font-weight: 300;
  font-size: 0.85em;
  color: rgba(245, 222, 179, 0.8);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-button {
  padding: 0 var(--spacing-md);
  background: transparent;
  border: none;
  border-left: 1px solid var(--primary-color-dim);
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-item:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background: var(--alert-color);
}

.delete-icon {
  position: relative;
  width: 16px;
  height: 16px;
}

.slide-in {
  animation: slideIn 0.3s ease both;
  animation-delay: var(--delay);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(var(--distance));
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
