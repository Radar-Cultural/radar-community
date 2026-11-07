<template>
  <a class="brand" href="/" aria-label="Radar Cultural, página de inicio">
    <svg class="brand__mark" viewBox="0 0 48 48" aria-hidden="true">
      <path class="brand__arc brand__arc--outer" d="M8 35A19 19 0 1 1 40 14" />
      <path class="brand__arc brand__arc--middle" d="M13 32A14 14 0 1 1 35 15" />
      <path class="brand__arc brand__arc--inner" d="M18 29A8.5 8.5 0 1 1 31 18" />
      <path class="brand__needle" d="m24 24 13-12" />
      <circle class="brand__core" cx="24" cy="24" r="3.4" />
    </svg>
    <span class="brand__name">Radar Cultural</span>
  </a>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.72rem;
  color: var(--color-text);
  font-family: var(--font-display);
  font-size: clamp(1.15rem, 1.6vw, 1.45rem);
  font-weight: 680;
  letter-spacing: -0.01em;
  text-decoration: none;
}

.brand__mark {
  width: 2.8rem;
  height: 2.8rem;
  overflow: visible;
}

.brand__arc {
  fill: none;
  stroke-linecap: round;
  stroke-width: 2.8;
}

.brand__arc--outer,
.brand__arc--inner {
  stroke: var(--color-violet);
}

.brand__arc--middle {
  stroke: var(--color-jade);
}

.brand__needle {
  fill: none;
  stroke: var(--color-coral);
  stroke-linecap: round;
  stroke-width: 2.7;
}

.brand__mark .brand__core {
  fill: var(--color-coral);
  stroke: none;
}

.brand:focus-visible {
  outline: 2px solid var(--color-violet);
  outline-offset: 0.45rem;
  border-radius: 0.2rem;
}

@media (max-width: 520px) {
  .brand__mark {
    width: 2.45rem;
    height: 2.45rem;
  }

  .brand__name {
    max-width: 7rem;
    line-height: 0.95;
  }
}
</style>
