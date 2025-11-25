<script setup lang="ts">
import { Icon } from '@iconify/vue'

// emit //
const emit = defineEmits<{
  (e: 'new'): void
  (e: 'close'): void
}>()
</script>

<template>
  <div class="sidebar-header">
    <h2>Chat History</h2>
    <div class="header-actions">
      <button class="new-chat-button" aria-label="New chat" @click="emit('new')">
        <Icon icon="material-symbols:add" style="color: var(--primary-color)" width="20" height="20" />
      </button>
      <button class="close-button" aria-label="Close chat history" @click="emit('close')">
        <Icon icon="material-symbols:chevron-left" style="color: var(--primary-color)" width="20" height="20" />
      </button>
    </div>
  </div>
</template>

<style scoped lang="css">
.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--primary-color-dim);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h2 {
  font-size: 1.3em;
  margin: 0;
  color: var(--primary-color);
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.new-chat-button,
.close-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--primary-color-bright);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.new-chat-button:hover,
.close-button:hover {
  background: rgba(245, 222, 179, 0.1);
}
</style>
