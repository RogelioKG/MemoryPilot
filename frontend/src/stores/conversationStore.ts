import type { Conversation, Message } from '../types'
import { defineStore } from 'pinia'
import { BlockService } from '../services/blockService'
import { MessageService } from '../services/messageService'

export const useConversationStore = defineStore('conversation', {
  state: () => {
    const firstConv: Conversation = {
      id: crypto.randomUUID(),
      title: 'Welcome Chat',
      timestamp: new Date(),
      messages: [
        MessageService.createSimple('system', '嗨，我可以為你做些什麼呢？'),
      ],
    }

    return {
      conversations: [firstConv],
      currentConversation: firstConv,
    }
  },

  actions: {
    createConversation(title?: string) {
      const conv: Conversation = {
        id: crypto.randomUUID(),
        title: title ?? `Chat ${this.conversations.length + 1}`,
        timestamp: new Date(),
        messages: [],
      }
      this.conversations.unshift(conv)
      this.currentConversation = conv
      return conv
    },

    setCurrentById(id: string) {
      const conv = this.conversations.find(c => c.id === id)
      if (conv) {
        this.currentConversation = conv
      }
    },

    addMessageToCurrent(message: Message) {
      if (!this.currentConversation) {
        this.createConversation('New Chat')
      }
      this.currentConversation!.messages.push(message)
    },

    updateTitleForCurrentConversation(title: string) {
      if (this.currentConversation) {
        this.currentConversation.title = title
      }
    },

    async deleteConversation(id: string) {
      const index = this.conversations.findIndex(c => c.id === id)
      if (index === -1)
        return

      const conv = this.conversations[index]!

      // 先清理所有 blocks
      for (const msg of conv.messages) {
        if (!msg.blocks)
          continue
        for (const block of msg.blocks) {
          if (block.kind === 'file') {
            await BlockService.deleteFileBlock(block)
          }
        }
      }

      // 再刪除 conversation
      this.conversations.splice(index, 1)

      // 再調整 currentConversation
      if (this.currentConversation?.id === id) {
        this.currentConversation
          = this.conversations[0] ?? this.createConversation('New Chat')
      }
    },

  },
})
