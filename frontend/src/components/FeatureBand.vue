<script setup lang="ts">
const features = [
  {
    title: 'Difusión cultural gratuita',
    accent: 'coral',
    icon: 'signal',
  },
  {
    title: 'Datos abiertos e interoperables',
    accent: 'turquoise',
    icon: 'layers',
  },
  {
    title: 'Tecnología para acercar la cultura',
    accent: 'lime',
    icon: 'orbit',
  },
] as const
</script>

<template>
  <section class="feature-band" aria-labelledby="principles-title">
    <h2 id="principles-title" class="visually-hidden">Principios de Radar Cultural</h2>
    <ul class="feature-band__list">
      <li
        v-for="feature in features"
        :key="feature.title"
        :class="`feature feature--${feature.accent}`"
      >
        <svg v-if="feature.icon === 'signal'" viewBox="0 0 48 48" aria-hidden="true">
          <circle cx="24" cy="24" r="17" />
          <circle cx="24" cy="24" r="9" />
          <circle class="fill" cx="24" cy="24" r="3" />
        </svg>
        <svg v-else-if="feature.icon === 'layers'" viewBox="0 0 48 48" aria-hidden="true">
          <path d="m8 18 16-9 16 9-16 9Z" />
          <path d="m8 26 16 9 16-9M8 34l16 9 16-9" />
        </svg>
        <svg v-else viewBox="0 0 48 48" aria-hidden="true">
          <circle cx="24" cy="24" r="15" stroke-dasharray="1 7" stroke-linecap="round" />
          <circle class="fill" cx="24" cy="24" r="2.5" />
        </svg>
        <p>{{ feature.title }}</p>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.feature-band {
  border-block: 1px solid var(--color-line);
}

.feature-band__list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin: 0;
  padding: 0;
  list-style: none;
}

.feature {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: clamp(1rem, 2.4vw, 2rem);
  min-height: 13rem;
  padding: clamp(2rem, 4vw, 3.8rem);
}

.feature + .feature {
  border-left: 1px solid var(--color-line);
}

.feature::after {
  position: absolute;
  right: clamp(2rem, 4vw, 3.8rem);
  bottom: 2.15rem;
  left: clamp(2rem, 4vw, 3.8rem);
  height: 1px;
  content: '';
  background: currentColor;
  opacity: 0.75;
}

.feature svg {
  width: 3.2rem;
  color: inherit;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
}

.feature svg .fill {
  fill: currentColor;
  stroke: none;
}

.feature p {
  max-width: 14rem;
  margin: 0;
  color: var(--color-text);
  font-size: clamp(1.05rem, 1.45vw, 1.35rem);
  line-height: 1.35;
}

.feature--coral {
  color: var(--color-coral);
}

.feature--turquoise {
  color: var(--color-turquoise);
}

.feature--lime {
  color: var(--color-lime);
}

@media (max-width: 820px) {
  .feature-band__list {
    grid-template-columns: 1fr;
  }

  .feature {
    min-height: 9rem;
  }

  .feature + .feature {
    border-top: 1px solid var(--color-line);
    border-left: 0;
  }
}
</style>
