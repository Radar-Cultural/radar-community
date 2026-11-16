<script setup lang="ts">
import BrandMark from './BrandMark.vue'
import ThemeToggle from './ThemeToggle.vue'
</script>

<template>
  <footer class="site-footer">
    <div class="site-footer__inner page-width">
      <BrandMark />
      <p>La cultura sucede. Que nadie se la pierda.</p>
      <nav aria-label="Enlaces del pie">
        <a href="/agenda/">Agenda</a>
        <a href="/privacidad/">Privacidad</a>
        <a href="/terminos/">Términos</a>
        <a href="/codigo-de-conducta/">Código de conducta</a>
        <a href="https://github.com/Radar-Cultural/radar-community" target="_blank" rel="noreferrer"
          >GitHub</a
        >
        <a
          href="https://github.com/Radar-Cultural/radar-community/security"
          target="_blank"
          rel="noreferrer"
          >Seguridad</a
        >
      </nav>
      <ThemeToggle />
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  color: var(--text);
  background: var(--canvas);
}
.site-footer__inner {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: clamp(1.3rem, 3vw, 3.2rem);
  align-items: center;
  min-height: 7rem;
  border-top: 1px solid var(--line);
}
.site-footer p {
  margin: 0;
  padding-left: clamp(1.2rem, 2.6vw, 2.8rem);
  border-left: 1px solid var(--line);
  font-size: 0.86rem;
}
.site-footer nav {
  display: flex;
  gap: clamp(1rem, 2vw, 2.2rem);
}
.site-footer nav a {
  display: inline-flex;
  align-items: center;
  min-height: 2.75rem;
  color: inherit;
  font-size: 0.84rem;
  text-decoration: none;
}
.site-footer nav a:hover {
  color: var(--wine);
}
@media (max-width: 930px) {
  .site-footer__inner {
    grid-template-columns: 1fr auto;
    padding-block: 2rem;
  }
  .site-footer p,
  .site-footer nav {
    grid-column: 1 / -1;
  }
  .site-footer p {
    padding-left: 0;
    border: 0;
  }
  .site-footer nav {
    flex-wrap: wrap;
  }
}
</style>
