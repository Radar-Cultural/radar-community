<script setup lang="ts">
import BrandMark from './BrandMark.vue'
import ThemeToggle from './ThemeToggle.vue'
</script>

<template>
  <footer class="site-footer">
    <div class="site-footer__inner page-width">
      <BrandMark />
      <nav aria-label="Enlaces del pie">
        <a href="#vision">Proyecto</a>
        <a
          href="https://github.com/Radar-Cultural/radar-community/blob/main/CONTRIBUTING.md"
          target="_blank"
          rel="noreferrer"
          >Contribuir</a
        >
        <a
          href="https://github.com/Radar-Cultural/radar-community/security"
          target="_blank"
          rel="noreferrer"
          >Seguridad</a
        >
      </nav>
      <p>Cultura abierta. Tecnología responsable.</p>
      <ThemeToggle />
      <a class="back-top" href="#contenido" aria-label="Volver al inicio">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 15 6-6 6 6" /></svg>
      </a>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  color: #f2f4f7;
  background:
    repeating-radial-gradient(
      circle at 70% 130%,
      transparent 0 5rem,
      rgb(255 255 255 / 0.04) 5.05rem 5.1rem
    ),
    #611232;
}

.site-footer__inner {
  display: grid;
  grid-template-columns: 1.1fr auto 1fr auto auto;
  gap: clamp(1.5rem, 4vw, 4.5rem);
  align-items: center;
  min-height: 9rem;
}

.site-footer :deep(.brand) {
  color: #f2f4f7;
}

.site-footer nav {
  display: flex;
  gap: clamp(1rem, 2.5vw, 2.5rem);
}

.site-footer nav a {
  padding-block: 0.35rem;
  border-bottom: 1px solid transparent;
  color: #f2f4f7;
  font-size: 0.9rem;
  text-decoration: none;
}

.site-footer nav a:hover,
.site-footer nav a:focus-visible {
  border-color: #c9993e;
}

.site-footer p {
  margin: 0;
  color: #e5ccd7;
  font-family: var(--font-display);
  font-size: clamp(1rem, 1.4vw, 1.25rem);
  font-style: italic;
}

.back-top {
  display: grid;
  place-items: center;
  width: 2.8rem;
  aspect-ratio: 1;
  border: 1px solid #c9993e;
  border-radius: 50%;
  color: #f2f4f7;
  transition: transform 200ms var(--ease-bounce);
}

.back-top:hover {
  transform: translateY(-0.25rem);
}

.back-top svg {
  width: 1.2rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

@media (max-width: 980px) {
  .site-footer__inner {
    grid-template-columns: 1fr auto;
    padding-block: 2.5rem;
  }

  .site-footer nav,
  .site-footer p {
    grid-column: 1 / -1;
  }

  .site-footer :deep(.theme-toggle) {
    grid-column: 1;
  }
  .back-top {
    grid-column: 2;
    grid-row: 3;
  }
}

@media (max-width: 560px) {
  .site-footer nav {
    flex-wrap: wrap;
  }
}
</style>
