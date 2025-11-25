import type { FileTypes } from '../../types'

export function checkFileTypes(types: string | string[], fileTypes?: FileTypes): boolean {
  if (!fileTypes)
    return true

  const arr = Array.isArray(types) ? types : [types]

  return typeof fileTypes === 'function'
    ? fileTypes(arr)
    : fileTypes.some(type => arr.includes(type))
}

export function filterFiles(files: File[], fileTypes?: FileTypes): File[] {
  return files.filter(file => checkFileTypes(file.type, fileTypes))
}

export function extractFiles(event: Event, fileTypes?: FileTypes): File[] {
  const input = event.target as HTMLInputElement
  const files = input.files ? Array.from(input.files) : []

  // Reset (avoid same files upload not triggering change)
  input.value = ''

  const filtered = filterFiles(files, fileTypes)

  if (filtered.length === 0) {
    alert('Please upload valid files!')
  }

  return filtered
}
