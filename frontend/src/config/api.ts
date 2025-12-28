export const API_BASE = {
  backend: import.meta.env.VITE_BACKEND_BASE_URL,
  dicebear: 'https://api.dicebear.com/7.x',
} as const

export const API = {
  avatar: {
    system: `${API_BASE.dicebear}/bottts/svg?seed=system`,
    user: `${API_BASE.dicebear}/avataaars/svg?seed=chickenattack`,
  },

  backend: {
    chat: `${API_BASE.backend}/chat`,
    chatStream: `${API_BASE.backend}/chat/stream`,
  },
} as const
