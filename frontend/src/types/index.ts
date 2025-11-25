export type FileTypes = string[] | ((types: readonly string[]) => boolean)

export type Sender = 'system' | 'user'

export type AvatarSize = 'sm' | 'md' | 'lg'

export interface FileBlock {
  id: string
  kind: 'file'
  name: string
  mime: string
  url: string
}

export interface CardBlock {
  id: string
  kind: 'card'
  info: string
}

export type MessageBlock = FileBlock | CardBlock

export interface Message {
  id: string
  text: string
  sender: Sender
  timestamp: Date
  blocks?: MessageBlock[]
  avatarUrl?: string
}

export interface Conversation {
  id: string
  title: string
  timestamp: Date
  messages: Message[]
}

export interface DBFile {
  id: string
  mime: string
  blob: Blob
}
