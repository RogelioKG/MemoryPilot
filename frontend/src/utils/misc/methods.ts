export const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0

export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}
