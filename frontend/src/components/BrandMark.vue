<template>
  <a class="brand" href="/" aria-label="Radar Cultural, inicio">
    <span>Radar Cultural</span>
  </a>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  justify-self: start;
  width: max-content;
  min-height: 2.75rem;
  color: inherit;
  font-family: var(--display);
  font-size: clamp(1.35rem, 2vw, 1.85rem);
  font-weight: 720;
  line-height: 1;
  letter-spacing: -0.055em;
  text-decoration: none;
}

.brand:focus-visible {
  border-radius: 0.2rem;
}

@media (max-width: 420px) {
  .brand {
    font-size: 1.25rem;
  }
}
</style>
