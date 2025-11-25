import { API } from '../config/api'
import { http } from './http'

export function buildChatForm(
  threadId: string,
  query: string,
  files?: File[],
) {
  const form = new FormData()
  form.append('query', query)
  form.append('thread_id', threadId)

  if (files) {
    files.forEach(f => form.append('files', f))
  }

  return form
}

export class ChatAPI {
  /**
   * 非串流模式
   */
  async chat(threadId: string, query: string, files?: File[]): Promise<string> {
    const form = buildChatForm(threadId, query, files)
    const response = await http.postForm(API.backend.chat, form)
    const result = await response.json()
    return result.answer
  }

  /**
   * 串流模式
   */
  async chatStream(
    threadId: string,
    query: string,
    files: File[] | undefined,
    onChunk: (text: string) => void,
  ): Promise<void> {
    const form = buildChatForm(threadId, query, files)
    const reader = await http.postStream(API.backend.chatStream, form)
    const decoder = new TextDecoder()

    while (true) {
      const { value, done } = await reader.read()
      if (done)
        break
      onChunk(decoder.decode(value))
    }
  }
}

export const chatAPI = new ChatAPI()
