<script setup lang="ts">
import type { AvatarSize } from '../../types'
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    src?: string
    name: string
    size?: AvatarSize
  }>(),
  {
    size: 'md',
    src: undefined,
  },
)

function generateInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const initials = computed(() => generateInitials(props.name))
const sizeClass = computed(() => `avatar-${props.size}`)
</script>

<template>
  <div class="avatar" :class="sizeClass">
    <img v-if="src" :src="src">
    <div v-else class="avatar-initials">
      {{ initials }}
    </div>
  </div>
</template>

<style scoped lang="css">
.avatar {
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--primary-color-dim);
  border: 2px solid var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  color: var(--primary-color);
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.avatar-sm {
  width: 32px;
  height: 32px;
  font-size: 0.8em;
}

.avatar-md {
  width: 40px;
  height: 40px;
  font-size: 1em;
}

.avatar-lg {
  width: 48px;
  height: 48px;
  font-size: 1.2em;
}
</style>
