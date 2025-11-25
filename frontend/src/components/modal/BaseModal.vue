<script setup lang="ts">
import { ref } from 'vue'

// ref //
const show = ref(false)

// methods //
function isShow() {
  return show.value
}

function showModal() {
  show.value = true
}

function closeModal() {
  show.value = false
}

defineExpose({
  isShow,
  showModal,
  closeModal,
})
</script>

<template>
  <Transition name="modal-outer">
    <div v-show="show" class="modal-wrapper" @click.self="closeModal()">
      <Transition name="modal-inner">
        <div v-if="show" class="modal">
          <slot name="header" />
          <slot name="body" />
          <slot name="footer" />
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<style scoped lang="css">
.modal-wrapper {
  position: absolute;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 8px;
  z-index: 10000;
}

.modal {
  position: relative;
  background-color: transparent;
  display: flex;
  flex-flow: column;
  align-items: center;
}

/* Tansition */
.modal-outer-enter-from,
.modal-outer-leave-to {
  opacity: 0;
}

.modal-outer-enter-active,
.modal-outer-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.modal-outer-enter-to,
.modal-outer-leave-from {
  opacity: 1;
}

.modal-inner-enter-from {
  transform: translateY(100px);
}

.modal-inner-enter-active,
.modal-inner-leave-active {
  transition: all 0.3s ease-in-out;
}

.modal-inner-leave-to {
  transform: translateY(100px);
}
</style>
