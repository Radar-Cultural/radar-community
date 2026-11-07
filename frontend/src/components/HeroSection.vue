<script setup lang="ts">
import AsyncAction from './AsyncAction.vue'
import RadarScene from './RadarScene.vue'
</script>

<template>
  <section class="hero section-dark" aria-labelledby="hero-title">
    <div class="hero__inner page-width">
      <div class="hero__copy">
        <h1 id="hero-title">La cultura entra en tu <em>radar.</em></h1>
        <p class="hero__intro">
          Estamos construyendo un punto de encuentro para descubrir, compartir y preservar la vida
          cultural de México.
        </p>
        <div class="hero__actions">
          <AsyncAction href="#vision">Explorar la visión</AsyncAction>
          <AsyncAction
            href="https://github.com/Radar-Cultural/radar-community"
            variant="secondary"
            external
          >
            Ver el código
          </AsyncAction>
        </div>
        <p class="hero__status"><span aria-hidden="true"></span>Plataforma en desarrollo</p>
      </div>
      <RadarScene class="hero__scene" />
      <a class="hero__scroll" href="#vision" aria-label="Continuar a la visión de Radar Cultural">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
      </a>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 100svh;
  overflow: hidden;
  background:
    radial-gradient(circle at 78% 38%, rgb(109 74 255 / 0.12), transparent 27rem),
    radial-gradient(circle at 28% 88%, rgb(97 18 50 / 0.26), transparent 34rem), var(--color-ink);
}

.hero::after {
  position: absolute;
  right: -10%;
  bottom: -8rem;
  left: -10%;
  height: 10rem;
  border: 1px solid rgb(201 153 62 / 0.75);
  border-radius: 50% 50% 0 0;
  content: '';
  background: var(--color-wine);
  transform: scaleX(1.1);
}

.hero__inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(24rem, 0.83fr) minmax(30rem, 1.17fr);
  align-items: center;
  min-height: 100svh;
  padding-top: var(--header-height);
  padding-bottom: 4.5rem;
}

.hero__copy {
  position: relative;
  z-index: 3;
  padding-block: clamp(3.5rem, 9vh, 7rem);
}

.hero h1 {
  max-width: 9.2ch;
  margin: 0;
  color: #f2f4f7;
  font-family: var(--font-display);
  font-size: clamp(4.2rem, 7.25vw, 8rem);
  font-weight: 720;
  line-height: 0.92;
  letter-spacing: -0.064em;
}

.hero h1 em {
  color: var(--color-coral);
  font-style: normal;
}

.hero__intro {
  max-width: 38rem;
  margin: 2rem 0 0;
  color: #c8ccd6;
  font-size: clamp(1.08rem, 1.45vw, 1.32rem);
  line-height: 1.58;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 2.25rem;
}

.hero__status {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin: 1.6rem 0 0;
  color: #b6bbc8;
  font-size: 0.92rem;
}

.hero__status span {
  width: 0.52rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--color-jade);
  box-shadow: 0 0 0 0.35rem rgb(25 179 154 / 0.1);
}

.hero__scene {
  justify-self: end;
  margin-right: -7vw;
}

.hero__scroll {
  position: absolute;
  z-index: 5;
  bottom: 4.2rem;
  left: 50%;
  display: grid;
  place-items: center;
  width: 2.8rem;
  aspect-ratio: 1;
  border: 1px solid rgb(242 244 247 / 0.28);
  border-radius: 50%;
  color: #f2f4f7;
  background: rgb(13 19 33 / 0.5);
  transform: translateX(-50%);
  backdrop-filter: blur(12px);
  animation: scroll-bounce 2.4s ease-in-out infinite;
}

.hero__scroll svg {
  width: 1.15rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

@keyframes scroll-bounce {
  50% {
    transform: translate(-50%, 0.35rem);
  }
}

@media (max-width: 1100px) {
  .hero__inner {
    grid-template-columns: minmax(22rem, 0.9fr) minmax(25rem, 1.1fr);
  }

  .hero__scene {
    margin-right: -15vw;
  }
}

@media (max-width: 760px) {
  .hero__inner {
    grid-template-columns: minmax(0, 1fr);
    align-content: start;
    padding-top: calc(var(--header-height) + 2.6rem);
    padding-bottom: 6rem;
  }

  .hero__copy {
    min-width: 0;
    padding-block: 2.5rem 0;
  }

  .hero h1 {
    max-width: 8ch;
    font-size: clamp(3.9rem, 16.5vw, 6.1rem);
  }

  .hero__intro {
    margin-top: 1.5rem;
    font-size: 1.05rem;
  }

  .hero__scene {
    justify-self: center;
    margin-right: 0;
  }

  .hero__scroll {
    bottom: 3.2rem;
  }
}

@media (max-width: 520px) {
  .hero__actions {
    display: grid;
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero__scroll {
    animation: none;
  }
}
</style>
