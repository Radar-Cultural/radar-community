<script setup lang="ts">
const principles = [
  {
    title: 'Descubrir',
    copy: 'Explorar la vida cultural desde un solo lugar.',
    tone: 'violet',
  },
  {
    title: 'Compartir',
    copy: 'Difundir actividades sin costo para el público.',
    tone: 'coral',
  },
  {
    title: 'Conectar',
    copy: 'Relacionar espacios, personas y conocimiento.',
    tone: 'jade',
  },
] as const
</script>

<template>
  <section id="vision" class="vision section-pad" aria-labelledby="vision-title">
    <div v-reveal class="vision__intro page-width">
      <h2 id="vision-title">Una agenda para <em>encontrarnos</em></h2>
      <p>
        Radar Cultural acercará actividades, recintos y comunidades mediante una experiencia clara,
        abierta y accesible.
      </p>
    </div>

    <div v-reveal class="orbit page-width">
      <svg class="orbit__line" viewBox="0 0 1200 280" preserveAspectRatio="none" aria-hidden="true">
        <path d="M20 220C210 80 390 255 610 120S970 70 1180 190" />
      </svg>
      <ol class="orbit__points">
        <li
          v-for="(principle, index) in principles"
          :key="principle.title"
          :class="`orbit-point orbit-point--${principle.tone}`"
        >
          <span class="orbit-point__signal" aria-hidden="true"><span></span></span>
          <div>
            <h3>{{ principle.title }}</h3>
            <p>{{ principle.copy }}</p>
          </div>
          <span class="visually-hidden">Principio {{ index + 1 }} de {{ principles.length }}</span>
        </li>
      </ol>
      <div class="orbit__artifact orbit__artifact--stone" aria-hidden="true"></div>
      <div class="orbit__artifact orbit__artifact--weave" aria-hidden="true"></div>
    </div>
  </section>
</template>

<style scoped>
.vision {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 70% 32%, rgb(109 74 255 / 0.1), transparent 30rem), var(--color-bg);
}

.vision::before,
.vision::after {
  position: absolute;
  border: 1px solid var(--color-line);
  border-radius: 50%;
  content: '';
  pointer-events: none;
}

.vision::before {
  top: -19rem;
  right: -12rem;
  width: 42rem;
  height: 42rem;
}

.vision::after {
  bottom: -23rem;
  left: -14rem;
  width: 46rem;
  height: 46rem;
}

.vision__intro {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(18rem, 0.6fr);
  gap: clamp(3rem, 8vw, 9rem);
  align-items: end;
}

.vision h2 {
  max-width: 12ch;
  margin: 0;
  color: var(--color-text);
  font-family: var(--font-display);
  font-size: clamp(3.4rem, 6.7vw, 7.2rem);
  line-height: 0.93;
  letter-spacing: -0.055em;
}

.vision h2 em {
  color: var(--color-wine-accent);
  font-style: italic;
  font-weight: 620;
}

.vision__intro > p {
  max-width: 32rem;
  margin: 0 0 0.6rem;
  color: var(--color-muted);
  font-size: clamp(1.05rem, 1.5vw, 1.28rem);
  line-height: 1.62;
}

.orbit {
  position: relative;
  min-height: 35rem;
  margin-top: clamp(4rem, 8vw, 8rem);
}

.orbit__line {
  position: absolute;
  z-index: 0;
  inset: 10% 0 auto;
  width: 100%;
  height: 17.5rem;
  overflow: visible;
}

.orbit__line path {
  fill: none;
  stroke: url(#unused);
  stroke: var(--color-violet);
  stroke-width: 2.2;
  vector-effect: non-scaling-stroke;
  filter: drop-shadow(0 0 0.55rem rgb(109 74 255 / 0.3));
}

.orbit__points {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: clamp(2rem, 7vw, 8rem);
  margin: 0;
  padding: 0;
  list-style: none;
}

.orbit-point {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  align-items: start;
  max-width: 21rem;
  transition: transform 250ms var(--ease-bounce);
}

.orbit-point:nth-child(1) {
  margin-top: 10rem;
}
.orbit-point:nth-child(2) {
  margin-top: 2.5rem;
}
.orbit-point:nth-child(3) {
  margin-top: 8.2rem;
}

.orbit-point:hover {
  transform: translateY(-0.5rem);
}

.orbit-point__signal {
  display: grid;
  place-items: center;
  width: 2.2rem;
  aspect-ratio: 1;
  margin-top: 0.3rem;
  border: 1px solid currentColor;
  border-radius: 50%;
  box-shadow: 0 0 0 0.55rem color-mix(in srgb, currentColor 10%, transparent);
}

.orbit-point__signal span {
  width: 0.62rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: currentColor;
}

.orbit-point--violet {
  color: var(--color-violet);
}
.orbit-point--coral {
  color: var(--color-coral);
}
.orbit-point--jade {
  color: var(--color-jade);
}

.orbit-point h3 {
  margin: 0;
  color: var(--color-text);
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3vw, 2.7rem);
  line-height: 1;
}

.orbit-point p {
  max-width: 16rem;
  margin: 0.7rem 0 0;
  color: var(--color-muted);
  line-height: 1.55;
}

.orbit__artifact {
  position: absolute;
  z-index: 0;
  border-radius: 50%;
  opacity: 0.38;
  filter: saturate(0.75);
}

.orbit__artifact--stone {
  right: -8rem;
  bottom: -11rem;
  width: 24rem;
  height: 24rem;
  background:
    repeating-conic-gradient(from 10deg, rgb(97 18 50 / 0.3) 0 8deg, transparent 8deg 16deg),
    repeating-radial-gradient(circle, var(--color-line-strong) 0 1px, transparent 1px 1rem);
}

.orbit__artifact--weave {
  bottom: -7rem;
  left: -8rem;
  width: 18rem;
  height: 18rem;
  background: repeating-linear-gradient(
    45deg,
    var(--color-coral) 0 0.6rem,
    var(--color-jade) 0.6rem 1.2rem,
    var(--color-wine) 1.2rem 1.8rem
  );
  mask-image: repeating-linear-gradient(-45deg, #000 0 0.35rem, transparent 0.35rem 0.7rem);
}

@media (max-width: 760px) {
  .vision__intro {
    grid-template-columns: 1fr;
    gap: 1.6rem;
  }

  .vision h2 {
    max-width: 10ch;
    font-size: clamp(3.2rem, 14vw, 5.2rem);
  }

  .orbit {
    min-height: auto;
    margin-top: 4rem;
  }

  .orbit__line {
    top: 0;
    left: 0.8rem;
    width: 2px;
    height: 100%;
    background: linear-gradient(var(--color-violet), var(--color-coral), var(--color-jade));
  }

  .orbit__line path {
    display: none;
  }

  .orbit__points {
    grid-template-columns: 1fr;
    gap: 3.6rem;
    padding-left: 0.1rem;
  }

  .orbit-point:nth-child(n) {
    margin-top: 0;
  }

  .orbit-point__signal {
    background: var(--color-bg);
  }

  .orbit__artifact {
    display: none;
  }
}
</style>
