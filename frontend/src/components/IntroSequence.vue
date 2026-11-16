<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const visible = ref(false)
let timer = 0

onMounted(() => {
  if (
    window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
    window.sessionStorage.getItem('radar-intro-seen')
  )
    return

  visible.value = true
  window.sessionStorage.setItem('radar-intro-seen', 'true')
  timer = window.setTimeout(() => {
    visible.value = false
  }, 1050)
})

onBeforeUnmount(() => window.clearTimeout(timer))
</script>

<template>
  <Transition name="intro">
    <div v-if="visible" class="intro" aria-hidden="true">
      <p><span>Radar</span> Cultural</p>
      <div class="intro__line"><span></span></div>
    </div>
  </Transition>
</template>

<style scoped>
.intro {
  position: fixed;
  z-index: 5000;
  inset: 0;
  display: grid;
  place-content: center;
  justify-items: center;
  color: var(--white);
  background: var(--ink);
  pointer-events: none;
}

.intro p {
  margin: 0;
  overflow: hidden;
  font-family: var(--display);
  font-size: clamp(2.3rem, 5vw, 4.2rem);
  font-weight: 500;
  letter-spacing: -0.025em;
  animation: intro-word 700ms 180ms var(--ease-out) both;
}

.intro p span {
  font-weight: 700;
}

.intro__line {
  position: relative;
  overflow: hidden;
  width: min(18rem, 54vw);
  height: 1px;
  margin-top: 1.2rem;
  background: rgb(247 248 250 / 0.25);
}

.intro__line span {
  display: block;
  width: 38%;
  height: 100%;
  background: var(--blue);
  animation: intro-line 800ms 180ms var(--ease-out) both;
}

.intro-leave-active {
  transition:
    clip-path 520ms var(--ease-out),
    opacity 360ms ease;
}

.intro-leave-to {
  opacity: 0;
  clip-path: inset(0 0 100% 0);
}

@keyframes intro-word {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
}

@keyframes intro-line {
  from {
    transform: translateX(-110%);
  }
  to {
    transform: translateX(265%);
  }
}
</style>
