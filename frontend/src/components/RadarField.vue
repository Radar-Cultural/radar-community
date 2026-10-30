<script setup lang="ts">
import radarImage from '../assets/mexico-radar.webp'
</script>

<template>
  <figure class="radar-field" aria-label="Radar sobre un mapa de México">
    <div class="radar-field__grid" aria-hidden="true"></div>
    <img
      class="radar-field__map"
      :src="radarImage"
      width="1200"
      height="800"
      alt="Mapa punteado de México atravesado por señales de radar"
      fetchpriority="high"
    />
    <div class="radar-field__pulse" aria-hidden="true"></div>
  </figure>
</template>

<style scoped>
.radar-field {
  position: relative;
  width: min(58vw, 51rem);
  aspect-ratio: 3 / 2;
  margin: 0;
  isolation: isolate;
}

.radar-field__map {
  position: absolute;
  inset: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0.88;
  filter: saturate(0.92) contrast(1.05);
}

.radar-field__grid {
  position: absolute;
  inset: 10% 4%;
  background-image: radial-gradient(circle, rgb(128 167 170 / 0.34) 0.7px, transparent 0.8px);
  background-size: 12px 12px;
  mask-image: radial-gradient(circle at 58% 48%, #000 10%, transparent 72%);
}

.radar-field__pulse {
  position: absolute;
  z-index: 2;
  top: 49.5%;
  left: 51.5%;
  width: 0.55rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--color-text);
  box-shadow: 0 0 0 0 rgb(217 232 90 / 0.45);
  animation: pulse 3.6s ease-out infinite;
}

@keyframes pulse {
  0%,
  35% {
    box-shadow: 0 0 0 0 rgb(217 232 90 / 0.4);
  }

  70%,
  100% {
    box-shadow: 0 0 0 1.4rem rgb(217 232 90 / 0);
  }
}

@media (max-width: 760px) {
  .radar-field {
    width: min(118vw, 38rem);
    margin-inline: -17vw -1rem;
  }

  .radar-field__pulse {
    width: 0.42rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .radar-field__pulse {
    animation: none;
    box-shadow: 0 0 0 0.55rem rgb(217 232 90 / 0.08);
  }
}
</style>
