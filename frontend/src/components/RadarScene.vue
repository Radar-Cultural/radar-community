<script setup lang="ts">
import radarImage from '../assets/mexico-radar.webp'

function updateDepth(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  const x = ((event.clientX - rect.left) / rect.width - 0.5) * 2
  const y = ((event.clientY - rect.top) / rect.height - 0.5) * 2
  target.style.setProperty('--pointer-x', x.toFixed(3))
  target.style.setProperty('--pointer-y', y.toFixed(3))
}

function resetDepth(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  target.style.setProperty('--pointer-x', '0')
  target.style.setProperty('--pointer-y', '0')
}
</script>

<template>
  <figure
    class="radar-scene"
    aria-label="Mapa de México recorrido por una señal de radar cultural"
    @pointermove="updateDepth"
    @pointerleave="resetDepth"
  >
    <div class="radar-scene__rings" aria-hidden="true">
      <span class="radar-scene__sweep"></span>
      <span class="radar-scene__core"></span>
    </div>
    <img
      class="radar-scene__map"
      :src="radarImage"
      width="1200"
      height="800"
      alt="Mapa punteado de México con señales culturales conectadas"
      fetchpriority="high"
    />
    <div class="cultural-fragment cultural-fragment--museum" aria-hidden="true">
      <svg viewBox="0 0 90 64">
        <path
          d="M8 52h74M14 47h62M20 43V25M33 43V25M45 43V25M57 43V25M70 43V25M14 20 45 7l31 13Z"
        />
      </svg>
    </div>
    <div class="cultural-fragment cultural-fragment--book" aria-hidden="true">
      <svg viewBox="0 0 90 64">
        <path
          d="M45 50c-8-7-18-10-32-9V12c14-1 24 3 32 10Zm0 0c8-7 18-10 32-9V12c-14-1-24 3-32 10Z"
        />
      </svg>
    </div>
    <div class="cultural-fragment cultural-fragment--stage" aria-hidden="true">
      <svg viewBox="0 0 90 64">
        <path d="M9 9h72v46H9Zm8 0c1 18 7 30 20 39M73 9c-1 18-7 30-20 39M34 43h22" />
      </svg>
    </div>
  </figure>
</template>

<style scoped>
.radar-scene {
  --pointer-x: 0;
  --pointer-y: 0;
  position: relative;
  width: min(57vw, 54rem);
  aspect-ratio: 1.15;
  margin: 0;
  isolation: isolate;
  transform: translate3d(calc(var(--pointer-x) * -0.25rem), calc(var(--pointer-y) * -0.18rem), 0);
  transition: transform 160ms ease-out;
}

.radar-scene::before {
  position: absolute;
  z-index: -2;
  inset: 8% 4%;
  border-radius: 50%;
  content: '';
  background: radial-gradient(circle, rgb(109 74 255 / 0.2), transparent 62%);
  filter: blur(2.5rem);
}

.radar-scene__map {
  position: absolute;
  z-index: 2;
  inset: 17% 1% 8%;
  width: 98%;
  height: 75%;
  object-fit: contain;
  filter: hue-rotate(10deg) saturate(1.12) contrast(1.06);
  transform: translate3d(calc(var(--pointer-x) * 0.4rem), calc(var(--pointer-y) * 0.3rem), 0);
  transition: transform 180ms ease-out;
}

.radar-scene__rings {
  position: absolute;
  z-index: 1;
  inset: 5%;
  border: 1px solid rgb(25 179 154 / 0.48);
  border-radius: 50%;
  background:
    linear-gradient(transparent 49.8%, var(--color-line-strong) 50%, transparent 50.2%),
    linear-gradient(90deg, transparent 49.8%, var(--color-line-strong) 50%, transparent 50.2%),
    repeating-radial-gradient(circle, transparent 0 10.8%, rgb(109 74 255 / 0.5) 11% 11.25%);
  overflow: hidden;
  mask-image: radial-gradient(circle, #000 0 66%, transparent 83%);
}

.radar-scene__sweep {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 47%;
  height: 47%;
  background: conic-gradient(from 182deg, rgb(25 179 154 / 0.62), transparent 72%);
  transform-origin: 0 0;
  animation: radar-sweep 7.5s linear infinite;
}

.radar-scene__core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0.7rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--color-jade);
  box-shadow:
    0 0 0 0.65rem rgb(25 179 154 / 0.08),
    0 0 1.4rem var(--color-jade);
  transform: translate(-50%, -50%);
  animation: core-pulse 2.8s ease-out infinite;
}

.cultural-fragment {
  position: absolute;
  z-index: 3;
  display: grid;
  place-items: center;
  width: clamp(5.7rem, 10vw, 9rem);
  aspect-ratio: 1.45;
  border: 1px solid var(--color-line-strong);
  border-radius: 1.1rem;
  background: linear-gradient(145deg, var(--color-acrylic-strong), var(--color-acrylic));
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(16px);
}

.cultural-fragment svg {
  width: 62%;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.7;
}

.cultural-fragment--museum {
  top: 10%;
  left: 15%;
  color: var(--color-violet-soft);
  transform: translate3d(calc(var(--pointer-x) * -0.85rem), calc(var(--pointer-y) * -0.65rem), 0)
    rotate(-5deg);
  animation: fragment-float 5.8s ease-in-out infinite;
}

.cultural-fragment--book {
  bottom: 7%;
  left: 17%;
  color: var(--color-coral);
  transform: translate3d(calc(var(--pointer-x) * -0.55rem), calc(var(--pointer-y) * -0.4rem), 0)
    rotate(4deg);
  animation: fragment-float 6.8s -1.3s ease-in-out infinite;
}

.cultural-fragment--stage {
  top: 18%;
  right: -1%;
  color: var(--color-gold);
  transform: translate3d(calc(var(--pointer-x) * 0.75rem), calc(var(--pointer-y) * 0.6rem), 0)
    rotate(4deg);
  animation: fragment-float 6.2s -2.1s ease-in-out infinite;
}

@keyframes radar-sweep {
  to {
    transform: rotate(1turn);
  }
}

@keyframes core-pulse {
  60%,
  100% {
    box-shadow:
      0 0 0 1.45rem rgb(25 179 154 / 0),
      0 0 1.4rem var(--color-jade);
  }
}

@keyframes fragment-float {
  50% {
    margin-top: -0.45rem;
  }
}

@media (max-width: 980px) {
  .radar-scene {
    width: min(65vw, 45rem);
  }
}

@media (max-width: 760px) {
  .radar-scene {
    width: min(125vw, 40rem);
    margin: -1rem -15vw -4rem;
  }

  .cultural-fragment--museum {
    top: 9%;
    left: 20%;
  }

  .cultural-fragment--stage {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .radar-scene,
  .radar-scene__map,
  .cultural-fragment {
    transform: none;
  }

  .radar-scene__sweep,
  .radar-scene__core,
  .cultural-fragment {
    animation: none;
  }
}
</style>
