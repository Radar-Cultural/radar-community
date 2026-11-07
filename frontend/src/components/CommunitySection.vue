<script setup lang="ts">
import AsyncAction from './AsyncAction.vue'

const paths = [
  {
    title: 'Código',
    copy: 'Construir una plataforma accesible y sostenible.',
    icon: 'code',
    tone: 'violet',
  },
  {
    title: 'Datos',
    copy: 'Mejorar catálogos, fuentes y estructuras abiertas.',
    icon: 'data',
    tone: 'coral',
  },
  {
    title: 'Cuidado',
    copy: 'Revisar accesibilidad, seguridad y calidad.',
    icon: 'care',
    tone: 'jade',
  },
] as const
</script>

<template>
  <section id="comunidad" class="community section-pad" aria-labelledby="community-title">
    <div class="community__inner page-width">
      <div v-reveal class="community__copy">
        <h2 id="community-title">Una comunidad que <em>amplifica</em> la cultura</h2>
        <p>
          Radar Community construye en abierto herramientas para documentar, difundir y conectar la
          actividad cultural.
        </p>
        <div class="community__actions">
          <AsyncAction href="https://github.com/Radar-Cultural/radar-community" external>
            Conocer Radar Community
          </AsyncAction>
          <a
            class="community__contribute"
            href="https://github.com/Radar-Cultural/radar-community/blob/main/CONTRIBUTING.md"
            target="_blank"
            rel="noreferrer"
          >
            Revisar cómo contribuir
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" /></svg>
          </a>
        </div>
        <p class="community__note">
          <span aria-hidden="true">&lt;/&gt;</span>
          El código y la documentación evolucionan mediante issues y pull requests.
        </p>
      </div>

      <div v-reveal class="community-signal">
        <div class="community-signal__rings" aria-hidden="true"><span></span></div>
        <article
          v-for="path in paths"
          :key="path.title"
          :class="`community-node community-node--${path.tone}`"
        >
          <span class="community-node__icon" aria-hidden="true">
            <svg v-if="path.icon === 'code'" viewBox="0 0 48 48">
              <path d="m17 13-11 11 11 11M31 13l11 11-11 11M28 7l-8 34" />
            </svg>
            <svg v-else-if="path.icon === 'data'" viewBox="0 0 48 48">
              <path d="m24 6 17 9-17 9-17-9Zm-17 18 17 9 17-9M7 33l17 9 17-9" />
            </svg>
            <svg v-else viewBox="0 0 48 48">
              <path d="M24 5 39 11v11c0 10-6 17-15 21C15 39 9 32 9 22V11Z" />
              <path d="m17 24 5 5 10-11" />
            </svg>
          </span>
          <h3>{{ path.title }}</h3>
          <p>{{ path.copy }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.community {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 73% 50%, rgb(109 74 255 / 0.09), transparent 28rem),
    var(--color-surface);
}

.community::before {
  position: absolute;
  top: -12rem;
  right: -8rem;
  width: 34rem;
  height: 34rem;
  border-radius: 50%;
  content: '';
  background: repeating-conic-gradient(
    from 30deg,
    color-mix(in srgb, var(--color-gold) 15%, transparent) 0 1deg,
    transparent 1deg 7deg
  );
  mask-image: radial-gradient(circle, transparent 0 42%, #000 42.5% 71%, transparent 71.5%);
}

.community__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(22rem, 0.78fr) minmax(34rem, 1.22fr);
  gap: clamp(3rem, 7vw, 7rem);
  align-items: center;
}

.community h2 {
  max-width: 10ch;
  margin: 0;
  color: var(--color-text);
  font-family: var(--font-display);
  font-size: clamp(3.5rem, 6.2vw, 6.8rem);
  line-height: 0.9;
  letter-spacing: -0.06em;
}

.community h2 em {
  color: var(--color-violet);
  font-style: italic;
  font-weight: 620;
}

.community__copy > p:not(.community__note) {
  max-width: 34rem;
  margin: 2rem 0 0;
  color: var(--color-muted);
  font-size: clamp(1.05rem, 1.45vw, 1.25rem);
  line-height: 1.62;
}

.community__actions {
  display: grid;
  justify-items: start;
  gap: 1.15rem;
  margin-top: 2.2rem;
}

.community__contribute {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.2rem;
  border-bottom: 1px solid var(--color-gold);
  color: var(--color-text);
  font-weight: 650;
  text-decoration: none;
}

.community__contribute svg {
  width: 1rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
  transition: transform 180ms ease;
}

.community__contribute:hover svg {
  transform: translate(0.18rem, -0.18rem);
}

.community__note {
  display: flex;
  gap: 0.8rem;
  align-items: center;
  max-width: 33rem;
  margin: 2.2rem 0 0;
  padding-top: 1.2rem;
  border-top: 1px solid var(--color-line);
  color: var(--color-muted);
  font-size: 0.91rem;
  line-height: 1.5;
}

.community__note span {
  color: var(--color-gold);
  font-family: var(--font-mono);
}

.community-signal {
  position: relative;
  min-height: 42rem;
}

.community-signal::before,
.community-signal::after {
  position: absolute;
  z-index: 0;
  content: '';
}

.community-signal::before {
  inset: 10%;
  border: 1px solid var(--color-line-strong);
  border-radius: 50%;
  background: radial-gradient(
    circle,
    color-mix(in srgb, var(--color-violet) 14%, transparent),
    transparent 66%
  );
}

.community-signal::after {
  top: 50%;
  right: 17%;
  left: 17%;
  height: 2px;
  background: linear-gradient(90deg, var(--color-coral), var(--color-violet), var(--color-jade));
}

.community-signal__rings {
  position: absolute;
  z-index: 1;
  top: 50%;
  left: 50%;
  display: grid;
  place-items: center;
  width: 14rem;
  aspect-ratio: 1;
  border: 1px solid color-mix(in srgb, var(--color-violet) 55%, transparent);
  border-radius: 50%;
  background: repeating-radial-gradient(
    circle,
    transparent 0 1.5rem,
    color-mix(in srgb, var(--color-violet) 23%, transparent) 1.55rem 1.6rem
  );
  transform: translate(-50%, -50%);
  animation: community-breathe 4s ease-in-out infinite;
}

.community-signal__rings span {
  width: 2rem;
  aspect-ratio: 1;
  border: 0.55rem solid var(--color-violet);
  border-radius: 50%;
  box-shadow: 0 0 2.2rem var(--color-violet);
}

.community-node {
  position: absolute;
  z-index: 2;
  width: min(15rem, 35%);
  padding: 1.35rem;
  border: 1px solid currentColor;
  border-radius: 1.4rem;
  background: var(--color-acrylic-strong);
  box-shadow: var(--shadow-md);
  text-align: center;
  backdrop-filter: blur(20px);
  transition: transform 260ms var(--ease-bounce);
}

.community-node:hover {
  transform: translateY(-0.5rem) scale(1.02);
}
.community-node--violet {
  top: 2%;
  left: 50%;
  color: var(--color-violet);
  transform: translateX(-50%);
}
.community-node--violet:hover {
  transform: translate(-50%, -0.5rem) scale(1.02);
}
.community-node--coral {
  bottom: 6%;
  left: 5%;
  color: var(--color-coral);
}
.community-node--jade {
  right: 5%;
  bottom: 6%;
  color: var(--color-jade);
}

.community-node__icon {
  display: grid;
  place-items: center;
  width: 3.6rem;
  aspect-ratio: 1;
  margin: -3.1rem auto 0;
  border-radius: 50%;
  color: #fff;
  background: currentColor;
  box-shadow: 0 0 0 0.6rem color-mix(in srgb, currentColor 12%, transparent);
}

.community-node__icon svg {
  width: 2rem;
  fill: none;
  stroke: #fff;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

.community-node h3 {
  margin: 1.2rem 0 0;
  color: var(--color-text);
  font-family: var(--font-display);
  font-size: 1.7rem;
}

.community-node p {
  margin: 0.55rem 0 0;
  color: var(--color-muted);
  font-size: 0.9rem;
  line-height: 1.48;
}

@keyframes community-breathe {
  50% {
    transform: translate(-50%, -50%) scale(1.045);
    opacity: 0.82;
  }
}

@media (max-width: 980px) {
  .community__inner {
    grid-template-columns: 1fr;
  }
  .community-signal {
    width: min(100%, 46rem);
    margin-inline: auto;
  }
}

@media (max-width: 560px) {
  .community h2 {
    font-size: clamp(3.3rem, 15vw, 5.2rem);
  }

  .community-signal {
    display: grid;
    gap: 2.8rem;
    min-height: auto;
    margin-top: 5rem;
  }

  .community-signal::before,
  .community-signal::after,
  .community-signal__rings {
    display: none;
  }

  .community-node,
  .community-node--violet,
  .community-node--coral,
  .community-node--jade {
    position: relative;
    inset: auto;
    width: 100%;
    transform: none;
  }

  .community-node:hover,
  .community-node--violet:hover {
    transform: translateY(-0.35rem);
  }
}

@media (prefers-reduced-motion: reduce) {
  .community-signal__rings {
    animation: none;
  }
}
</style>
