import type { DBSchema, IDBPDatabase } from 'idb'
import type { DBFile } from '../types'
import { openDB } from 'idb'

// -----------------------------
// DB Schema
// -----------------------------
interface ChatDBSchema extends DBSchema {
  files: {
    key: string
    value: DBFile
  }
}

const DB_NAME = 'ChatDB'
const DB_VERSION = 1

let dbPromise: Promise<IDBPDatabase<ChatDBSchema>> | null = null

// -----------------------------
// Open DB
// -----------------------------
export function getDB() {
  if (dbPromise)
    return dbPromise

  dbPromise = openDB<ChatDBSchema>(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains('files')) {
        db.createObjectStore('files', { keyPath: 'id' })
      }
    },
  })

  return dbPromise
}

// -----------------------------
// File CRUD
// -----------------------------
export async function addFile(file: DBFile): Promise<void> {
  const db = await getDB()
  await db.put('files', file)
}

export async function getFile(id: string): Promise<DBFile | undefined> {
  const db = await getDB()
  return db.get('files', id)
}

export async function deleteFile(id: string): Promise<void> {
  const db = await getDB()
  await db.delete('files', id)
}
