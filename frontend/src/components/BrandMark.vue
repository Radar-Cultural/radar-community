<template>
  <a class="brand" href="/" aria-label="Radar Cultural, página de inicio">
    <svg class="brand__mark" viewBox="0 0 48 48" aria-hidden="true">
      <circle cx="24" cy="24" r="20" />
      <circle cx="24" cy="24" r="11" />
      <path d="M24 24 38 12A19 19 0 0 1 43 24Z" />
      <circle class="brand__signal" cx="36" cy="17" r="2.5" />
      <circle class="brand__core" cx="24" cy="24" r="3" />
    </svg>
    <span>Radar Cultural</span>
  </a>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  color: var(--color-text);
  font-size: 0.98rem;
  font-weight: 650;
  letter-spacing: -0.01em;
  text-decoration: none;
}

.brand__mark {
  width: 2.4rem;
  height: 2.4rem;
  overflow: visible;
}

.brand__mark circle,
.brand__mark path {
  fill: none;
  stroke: var(--color-turquoise);
  stroke-width: 1.5;
}

.brand__mark path {
  fill: color-mix(in srgb, var(--color-turquoise) 18%, transparent);
  stroke: none;
}

.brand__mark .brand__signal {
  fill: var(--color-coral);
  stroke: none;
}

.brand__mark .brand__core {
  fill: var(--color-text);
  stroke: none;
}

.brand:focus-visible {
  outline: 2px solid var(--color-lime);
  outline-offset: 0.45rem;
  border-radius: 0.2rem;
}
</style>
