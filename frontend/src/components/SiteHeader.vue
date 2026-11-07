<script setup lang="ts">
import { ref } from 'vue'
import BrandMark from './BrandMark.vue'
import ThemeToggle from './ThemeToggle.vue'

const menuOpen = ref(false)

function closeMenu() {
  menuOpen.value = false
}
</script>

<template>
  <header class="site-header">
    <div class="site-header__inner page-width">
      <BrandMark />
      <nav
        id="site-navigation"
        class="site-nav"
        :class="{ 'site-nav--open': menuOpen }"
        aria-label="Principal"
      >
        <a href="#vision" @click="closeMenu">Visión</a>
        <a href="#datos" @click="closeMenu">Datos abiertos</a>
        <a href="#comunidad" @click="closeMenu">Comunidad</a>
      </nav>
      <div class="site-header__actions">
        <ThemeToggle />
        <button
          class="menu-toggle"
          type="button"
          :aria-expanded="menuOpen"
          aria-controls="site-navigation"
          :aria-label="menuOpen ? 'Cerrar menú' : 'Abrir menú'"
          @click="menuOpen = !menuOpen"
        >
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: absolute;
  z-index: 20;
  top: 0;
  right: 0;
  left: 0;
  color-scheme: dark;
  --color-text: #f2f4f7;
  --color-muted: #b8beca;
  --color-line: rgb(211 219 232 / 0.14);
  --color-line-strong: rgb(211 219 232 / 0.28);
  --color-acrylic: rgb(20 29 48 / 0.58);
  --color-acrylic-strong: rgb(25 35 57 / 0.9);
  --color-surface-muted: #182136;
}

.site-header__inner {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  min-height: var(--header-height);
  border-bottom: 1px solid var(--color-line);
}

.site-nav {
  display: flex;
  align-items: center;
  gap: clamp(1.4rem, 3vw, 3.1rem);
}

.site-nav a {
  position: relative;
  padding: 0.4rem 0;
  color: var(--color-muted);
  font-size: 0.94rem;
  font-weight: 610;
  text-decoration: none;
}

.site-nav a::after {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 1px;
  content: '';
  background: linear-gradient(90deg, var(--color-violet), var(--color-jade));
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 220ms var(--ease-out);
}

.site-nav a:hover,
.site-nav a:focus-visible {
  color: var(--color-text);
}

.site-nav a:hover::after,
.site-nav a:focus-visible::after {
  transform: scaleX(1);
  transform-origin: left;
}

.site-header__actions {
  display: flex;
  justify-self: end;
  align-items: center;
  gap: 0.75rem;
}

.menu-toggle {
  display: none;
  width: 2.7rem;
  height: 2.7rem;
  padding: 0.65rem;
  border: 1px solid var(--color-line-strong);
  border-radius: 0.8rem;
  background: var(--color-acrylic);
  cursor: pointer;
  backdrop-filter: blur(14px);
}

.menu-toggle span {
  display: block;
  height: 1.5px;
  margin-block: 0.27rem;
  border-radius: 2px;
  background: var(--color-text);
}

@media (max-width: 760px) {
  .site-header__inner {
    grid-template-columns: 1fr auto;
  }

  .menu-toggle {
    display: block;
  }

  .site-nav {
    position: absolute;
    top: calc(var(--header-height) - 0.35rem);
    right: var(--page-gutter);
    left: var(--page-gutter);
    display: grid;
    gap: 0;
    padding: 0.55rem;
    border: 1px solid var(--color-line-strong);
    border-radius: 1rem;
    background: var(--color-acrylic-strong);
    box-shadow: var(--shadow-lg);
    visibility: hidden;
    opacity: 0;
    transform: translateY(-0.5rem);
    transition:
      opacity 180ms ease,
      transform 180ms ease,
      visibility 180ms;
    backdrop-filter: blur(24px);
  }

  .site-nav--open {
    visibility: visible;
    opacity: 1;
    transform: translateY(0);
  }

  .site-nav a {
    padding: 0.9rem 1rem;
    border-radius: 0.65rem;
  }

  .site-nav a:hover,
  .site-nav a:focus-visible {
    background: var(--color-surface-muted);
  }
}
</style>
