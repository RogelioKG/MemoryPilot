<script setup lang="ts">
import type { Message } from '../../types'
import { Icon } from '@iconify/vue'
import DOMPurify from 'dompurify'
import { computed } from 'vue'
import { formatTime } from '../../utils/misc/date'
import Avatar from '../misc/Avatar.vue'

// props //
const props = defineProps<{
  message: Message
}>()

// computed //
// 防止 XSS 攻擊
const sanitizedMessageText = computed(() => {
  return DOMPurify.sanitize(props.message.text.replace(/\n/g, '<br>'))
})
</script>

<template>
  <div class="message" :class="{ 'message-own': message.sender === 'user' }">
    <Avatar
      v-if="message.sender !== 'user'" :name="message.sender" :src="message.avatarUrl" size="md"
      class="message-avatar"
    />
    <div class="message-content">
      <div class="message-header">
        <span class="sender">{{ message.sender }}</span>
        <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
      </div>
      <p class="message-text" v-html="sanitizedMessageText" />
      <div v-if="message.blocks && message.blocks.length" class="message-blocks">
        <div v-for="b in message.blocks.filter(b => b.kind === 'file')" :key="b.id">
          <img v-if="b.mime.startsWith('image')" :src="b.url" :alt="b.name" class="image-block">
          <a v-else :href="b.url" target="_blank" class="file-block">
            <Icon icon="material-symbols:lab-profile-sharp" width="24" height="24" />
            {{ b.name }}
          </a>
        </div>
      </div>
    </div>
    <Avatar
      v-if="message.sender === 'user'" :name="message.sender" :src="message.avatarUrl" size="md"
      class="message-avatar"
    />
  </div>
</template>

<style scoped lang="css">
.message {
  margin: var(--spacing-sm);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  animation: message-appear 0.3s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes message-appear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-content {
  background-color: rgba(255, 255, 255, 0.15);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  max-width: 60%;
  backdrop-filter: blur(1px);
  border: 1px solid var(--primary-color-brighter);
}

.message-own {
  justify-content: flex-end;
}

.message-own .message-content {
  background-color: var(--primary-color-dim);
  border-color: var(--primary-active-color-brighter);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--spacing-xs);
}

.sender {
  font-size: 1.1em;
  font-weight: bold;
  color: var(--primary-color);
}

.timestamp {
  font-size: 0.8em;
  color: var(--primary-color-bright);
  margin-left: var(--spacing-sm);
}

.message-text {
  font-size: 1.1em;
  font-weight: 300;
  margin: 0;
  word-wrap: break-word;
  color: var(--primary-color);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  line-height: 1.5;
}

.message-avatar {
  margin-top: var(--spacing-xs);
  animation: avatar-appear 0.3s ease-out forwards;
  opacity: 0;
  transform: scale(0.8);
}

@keyframes avatar-appear {
  from {
    opacity: 0;
    transform: scale(0.8);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

.message-blocks {
  display: flex;
  flex-direction: column;
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--primary-color-dim);
  gap: var(--spacing-sm);
}

.image-block {
  max-width: 100%;
  max-height: 300px;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.image-block:hover {
  transform: scale(1.015);
}

.file-block {
  display: block;
  padding: var(--spacing-md);
  color: var(--primary-color);
  border-radius: var(--border-radius-md);
  background-color: var(--primary-color-dim);
  text-decoration: none;
  font-size: 0.9em;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.file-block:hover {
  opacity: 1;
  text-decoration: underline;
}
</style>
