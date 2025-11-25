<script setup lang="ts">
import { MessageService } from '../../services/messageService'
import { useConversationStore } from '../../stores/conversationStore'
import ChatHeader from './ChatHeader.vue'
import ChatInput from './ChatInput.vue'
import ChatMessageList from './ChatMessageList.vue'
import ChatSidebar from './Sidebar.vue'

// emit //
const emit = defineEmits<{
  (e: 'send', payload: { message: string, files?: File[] }): void
}>()

const convStore = useConversationStore()

// 處理上傳訊息 (user) //
async function handleMessageSend(payload: { message: string, files?: File[] }) {
  const { message, files } = payload

  const userMessage = files
    ? await MessageService.createUpload('user', message, files)
    : await MessageService.createSimple('user', message)

  convStore.addMessageToCurrent(userMessage)

  emit('send', payload)
}
</script>

<template>
  <div class="chat-container">
    <ChatSidebar
      :conversations="convStore.conversations" :current-conversation="convStore.currentConversation!"
      @select="convStore.setCurrentById" @new="convStore.createConversation" @delete="convStore.deleteConversation"
    />
    <div class="chat-main">
      <ChatHeader
        :title="convStore.currentConversation.title"
        @update:title="convStore.updateTitleForCurrentConversation"
      />
      <ChatMessageList :messages="convStore.currentConversation.messages" />
      <ChatInput @send="handleMessageSend" />
    </div>
  </div>
</template>

<style scoped lang="css">
.chat-container {
  position: relative;
  height: 100%;
  width: 100%;
}

.chat-main {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 0 auto;
  background-color: transparent;
  z-index: 1;
}
</style>
