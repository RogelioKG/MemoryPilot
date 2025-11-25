import type { FileBlock } from '../types'
import { addFile, deleteFile } from '../db/fileDb'

export const BlockService = {

  async createFileBlock(file: File): Promise<FileBlock> {
    const id = crypto.randomUUID()

    await addFile({
      id,
      mime: file.type,
      blob: file,
    })

    const url = URL.createObjectURL(file)

    return {
      id,
      kind: 'file',
      name: file.name,
      mime: file.type,
      url,
    }
  },

  async deleteFileBlock(block: FileBlock) {
    if (block.url.startsWith('blob:')) {
      URL.revokeObjectURL(block.url)
    }
    await deleteFile(block.id)
  },
}
