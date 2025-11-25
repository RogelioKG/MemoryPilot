<script setup lang="ts">
import { chatAPI } from '../api/chat'
import ChatRoom from '../components/chat/ChatRoom.vue'
import { MessageService } from '../services/messageService'
import { useConversationStore } from '../stores/conversationStore'
import { sleep } from '../utils/misc/methods'

const convStore = useConversationStore()

// 處理來自 ChatRoom 的事件 (system)
async function handleUserMessage(payload: { message: string, files?: File[] }) {
  const { message, files } = payload

  const systemMessage = MessageService.createSimple('system', '')
  await sleep(500)
  convStore.addMessageToCurrent(systemMessage)

  await chatAPI.chatStream(
    convStore.currentConversation.id,
    message,
    files,
    (chunk) => {
      const sys = convStore.currentConversation.messages.find(message => message.id === systemMessage.id)!
      sys.text += chunk
    },
  )
}
</script>

<template>
  <main>
    <div class="jagged-bg" />
    <ChatRoom @send="handleUserMessage" />
  </main>
</template>

<style scoped lang="css">
@import url("../styles/jagged-bg.css");

main {
  width: 100%;
  height: 100%;
}
</style>
