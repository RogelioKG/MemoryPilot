import type { Message, Sender } from '../types'
import { API } from '../config/api'
import { BlockService } from './blockService'

export const MessageService = {
  createSimple(sender: Sender, text: string): Message {
    return {
      id: crypto.randomUUID(),
      text,
      sender,
      timestamp: new Date(),
      avatarUrl: API.avatar[sender],
    }
  },

  async createUpload(sender: Sender, text: string, files: File[]): Promise<Message> {
    const blocks = await Promise.all(
      files.map(file => BlockService.createFileBlock(file)),
    )
    return {
      id: crypto.randomUUID(),
      text,
      sender,
      timestamp: new Date(),
      avatarUrl: API.avatar[sender],
      blocks,
    }
  },
}
