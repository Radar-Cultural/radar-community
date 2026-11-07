<script setup lang="ts">
const layers = [
  { name: 'Event', caption: 'Actividad cultural', icon: 'calendar', tone: 'violet' },
  { name: 'Place', caption: 'Espacio y ubicación', icon: 'place', tone: 'coral' },
  { name: 'Organization', caption: 'Fuente responsable', icon: 'people', tone: 'jade' },
] as const
</script>

<template>
  <section id="datos" class="data section-pad" aria-labelledby="data-title">
    <div class="data__inner page-width">
      <div v-reveal class="data__copy">
        <h2 id="data-title">Datos que pueden <em>viajar</em></h2>
        <p>
          Estructuras interoperables para que la información cultural sea fácil de consultar,
          reutilizar y preservar.
        </p>
        <ul class="data__standards" aria-label="Principios de los datos">
          <li><span class="tone-violet"></span>Schema.org</li>
          <li><span class="tone-coral"></span>Datos abiertos</li>
          <li><span class="tone-jade"></span>Fuentes verificables</li>
        </ul>
      </div>

      <div v-reveal class="data-model" aria-label="Relación entre evento, lugar y organización">
        <div class="data-model__orbit" aria-hidden="true"></div>
        <article
          v-for="layer in layers"
          :key="layer.name"
          :class="`data-layer data-layer--${layer.tone}`"
        >
          <svg v-if="layer.icon === 'calendar'" viewBox="0 0 48 48" aria-hidden="true">
            <rect x="8" y="11" width="32" height="29" rx="4" />
            <path d="M15 7v8M33 7v8M8 20h32M16 27h4M27 27h4M16 34h4" />
          </svg>
          <svg v-else-if="layer.icon === 'place'" viewBox="0 0 48 48" aria-hidden="true">
            <path d="M38 20c0 10-14 21-14 21S10 30 10 20a14 14 0 1 1 28 0Z" />
            <circle cx="24" cy="20" r="5" />
          </svg>
          <svg v-else viewBox="0 0 48 48" aria-hidden="true">
            <circle cx="24" cy="16" r="7" />
            <circle cx="11" cy="21" r="4" />
            <circle cx="37" cy="21" r="4" />
            <path d="M11 38c1-8 6-12 13-12s12 4 13 12M3 37c1-6 4-9 9-9M45 37c-1-6-4-9-9-9" />
          </svg>
          <h3>{{ layer.name }}</h3>
          <p>{{ layer.caption }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.data {
  position: relative;
  overflow: hidden;
  color: #f2f4f7;
  background:
    radial-gradient(circle at 72% 48%, rgb(109 74 255 / 0.18), transparent 25rem),
    linear-gradient(155deg, #0d1321, #11172b 60%, #161128);
}

.data::before {
  position: absolute;
  inset: 0;
  content: '';
  background-image: radial-gradient(circle, rgb(242 244 247 / 0.12) 0 1px, transparent 1px);
  background-size: 2rem 2rem;
  mask-image: linear-gradient(90deg, transparent, #000 55%, transparent);
}

.data__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(20rem, 0.72fr) minmax(34rem, 1.28fr);
  gap: clamp(3rem, 7vw, 7rem);
  align-items: center;
}

.data h2 {
  max-width: 10ch;
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(3.5rem, 6vw, 6.6rem);
  line-height: 0.95;
  letter-spacing: -0.055em;
}

.data h2 em {
  color: var(--color-coral);
  font-style: italic;
  font-weight: 620;
}

.data__copy > p {
  max-width: 32rem;
  margin: 1.8rem 0 0;
  color: #c8ccd6;
  font-size: clamp(1.05rem, 1.4vw, 1.22rem);
  line-height: 1.65;
}

.data__standards {
  display: grid;
  gap: 0.8rem;
  margin: 2.2rem 0 0;
  padding: 0;
  list-style: none;
}

.data__standards li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #d9dce5;
}

.data__standards span {
  width: 0.55rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 0.35rem color-mix(in srgb, currentColor 12%, transparent);
}

.tone-violet {
  color: var(--color-violet-soft);
}
.tone-coral {
  color: var(--color-coral);
}
.tone-jade {
  color: var(--color-jade);
}

.data-model {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: center;
  min-height: 36rem;
  perspective: 80rem;
}

.data-model::before {
  position: absolute;
  z-index: 0;
  right: 3%;
  left: 3%;
  top: 50%;
  height: 2px;
  content: '';
  background: linear-gradient(90deg, var(--color-violet), var(--color-coral), var(--color-jade));
  box-shadow: 0 0 1.2rem rgb(109 74 255 / 0.45);
}

.data-model__orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30rem;
  aspect-ratio: 1;
  border: 1px solid rgb(134 112 255 / 0.28);
  border-radius: 50%;
  background: repeating-radial-gradient(
    circle,
    transparent 0 3.8rem,
    rgb(134 112 255 / 0.12) 3.85rem 3.9rem
  );
  transform: translate(-50%, -50%);
}

.data-layer {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  min-height: 17rem;
  padding: 2rem 1rem;
  border: 1px solid currentColor;
  border-radius: 1.3rem;
  background: linear-gradient(145deg, rgb(255 255 255 / 0.15), rgb(255 255 255 / 0.05));
  box-shadow: 0 1.8rem 4rem rgb(0 0 0 / 0.2);
  text-align: center;
  backdrop-filter: blur(22px);
  transition: transform 300ms var(--ease-bounce);
}

.data-layer:nth-of-type(1) {
  transform: translateX(1rem) rotateY(7deg);
}
.data-layer:nth-of-type(2) {
  z-index: 2;
  transform: translateY(1.4rem) scale(1.05);
}
.data-layer:nth-of-type(3) {
  transform: translateX(-1rem) rotateY(-7deg);
}

.data-layer:hover {
  z-index: 4;
  transform: translateY(-0.55rem) scale(1.045);
}
.data-layer--violet {
  color: #a793ff;
}
.data-layer--coral {
  color: #ff8585;
}
.data-layer--jade {
  color: #55dbc3;
}

.data-layer svg {
  width: 3.5rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.5;
}

.data-layer h3 {
  margin: 1rem 0 0;
  color: #f2f4f7;
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 2.4vw, 2.25rem);
}

.data-layer p {
  margin: 0.45rem 0 0;
  color: #c8ccd6;
  font-size: 0.9rem;
}

@media (max-width: 980px) {
  .data__inner {
    grid-template-columns: 1fr;
  }

  .data-model {
    min-height: 30rem;
  }
}

@media (max-width: 650px) {
  .data-model {
    grid-template-columns: 1fr;
    gap: 1rem;
    min-height: auto;
    margin-top: 1rem;
  }

  .data-model::before {
    top: 3%;
    bottom: 3%;
    left: 50%;
    width: 2px;
    height: auto;
  }

  .data-model__orbit {
    width: 22rem;
  }

  .data-layer {
    width: min(100%, 24rem);
    min-height: 11rem;
    margin-inline: auto;
  }

  .data-layer:nth-of-type(n) {
    transform: none;
  }
}
</style>
