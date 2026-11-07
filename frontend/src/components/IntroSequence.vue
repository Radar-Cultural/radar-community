<script setup lang="ts">
import { onMounted, ref } from 'vue'

const visible = ref(true)

onMounted(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  window.setTimeout(
    () => {
      visible.value = false
    },
    reduced ? 80 : 1180,
  )
})
</script>

<template>
  <Transition name="intro-fade">
    <div v-if="visible" class="intro" aria-hidden="true">
      <div class="intro__radar"><span></span></div>
      <p>Radar Cultural</p>
    </div>
  </Transition>
</template>

<style scoped>
.intro {
  position: fixed;
  z-index: 1000;
  inset: 0;
  display: grid;
  place-content: center;
  gap: 1.4rem;
  background: #0d1321;
}

.intro p {
  margin: 0;
  color: #f2f4f7;
  font-family: var(--font-display);
  font-size: 1.2rem;
  letter-spacing: 0.02em;
  animation: intro-copy 720ms 220ms both var(--ease-out);
}

.intro__radar {
  position: relative;
  width: 5rem;
  aspect-ratio: 1;
  margin-inline: auto;
  border: 1px solid rgb(109 74 255 / 0.6);
  border-radius: 50%;
  background: repeating-radial-gradient(
    circle,
    transparent 0 0.68rem,
    rgb(109 74 255 / 0.34) 0.72rem 0.76rem
  );
  overflow: hidden;
  animation: intro-scale 760ms both var(--ease-out);
}

.intro__radar::before {
  position: absolute;
  inset: 50% 50% 0;
  width: 50%;
  height: 50%;
  content: '';
  background: conic-gradient(from 180deg, rgb(25 179 154 / 0.8), transparent 68%);
  transform-origin: 0 0;
  animation: intro-scan 850ms 140ms both ease-in-out;
}

.intro__radar span {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0.45rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: #ff5b5b;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 1.4rem #ff5b5b;
}

.intro-fade-leave-active {
  transition:
    opacity 360ms ease,
    transform 500ms var(--ease-out);
}

.intro-fade-leave-to {
  opacity: 0;
  transform: scale(1.04);
}

@keyframes intro-scale {
  from {
    opacity: 0;
    transform: scale(0.55);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes intro-scan {
  from {
    transform: rotate(-120deg);
  }
  to {
    transform: rotate(220deg);
  }
}

@keyframes intro-copy {
  from {
    opacity: 0;
    transform: translateY(0.5rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
