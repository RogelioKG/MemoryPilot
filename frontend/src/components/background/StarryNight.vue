<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from 'vue'
import { createUniverse, initCanvas, setEndingSignal } from '../../utils/background/universe'
import Night from './Night.vue'

// ref //
const animationStart = ref(false)
const canvasRef = useTemplateRef<HTMLCanvasElement>('canvasRef')

// methods //
function initNightCanvas() {
  if (canvasRef.value) {
    initCanvas(canvasRef.value)
  }
}

function enableStarryEffect() {
  animationStart.value = true
  setEndingSignal(false)
  if (canvasRef.value) {
    createUniverse(canvasRef.value)
  }
}

function disableStarryEffect() {
  animationStart.value = false
  setEndingSignal(true)
}

// life cycle //
onMounted(() => {
  initNightCanvas()
})

// expose //
defineExpose({
  enableStarryEffect,
  disableStarryEffect,
})
</script>

<template>
  <div class="universe">
    <div class="universe-container" :class="{ night: animationStart }">
      <div class="content">
        <canvas id="universe" ref="canvasRef" />
        <div id="footer">
          <Night />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="css">
/* THE UNIVERSE. Code adapted from https://codepen.io/Acuetouag/pen/vOgmza */

.universe {
  display: flex;
  justify-content: center;
  align-items: center;
  filter: contrast(120%);
  background-color: black;
  padding: 0px;
  margin: 0px;
  width: 100%;
  height: 100%;
  background: radial-gradient(1600px at 70% 120%, rgba(33, 39, 80, 1) 10%, #020409 100%);
}

.universe-container {
  width: 100%;
  height: 100%;
  backdrop-filter: brightness(150%);
  transition: backdrop-filter 1s ease-in;
}

.night {
  backdrop-filter: brightness(100%);
}

.content {
  width: inherit;
  height: inherit;
}

#universe {
  width: 100%;
  height: 100%;
}

#footer {
  position: absolute;
  width: 100%;
  height: 300px;
  bottom: 0;
}
</style>
