<script setup lang="ts">
import { ref } from 'vue'
import BrandMark from './BrandMark.vue'
import ThemeToggle from './ThemeToggle.vue'

defineProps<{ home?: boolean }>()

const menuOpen = ref(false)
const closeMenu = () => {
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
        <a href="/agenda/" @click="closeMenu">Agenda</a>
        <a :href="home ? '#proyecto' : '/#proyecto'" @click="closeMenu">Cómo funciona</a>
        <a :href="home ? '#datos' : '/#datos'" @click="closeMenu">Datos abiertos</a>
        <a :href="home ? '#comunidad' : '/#comunidad'" @click="closeMenu">Comunidad</a>
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
  position: fixed;
  z-index: 100;
  top: clamp(0.7rem, 1.35vw, 1.15rem);
  right: 0;
  left: 0;
  color: var(--text);
  pointer-events: none;
}

.site-header__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  min-height: calc(var(--header) - 1.25rem);
  padding-inline: clamp(0.85rem, 1.45vw, 1.35rem);
  border: 1px solid color-mix(in srgb, var(--line-strong) 72%, transparent);
  border-radius: 1rem 1rem 0.78rem 0.78rem;
  background: transparent;
  box-shadow:
    0 1.1rem 3rem rgb(8 9 13 / 0.1),
    inset 0 1px 0 color-mix(in srgb, var(--text) 9%, transparent);
  pointer-events: auto;
}

.site-header__inner::before {
  position: absolute;
  z-index: 0;
  inset: 0;
  border-radius: inherit;
  content: '';
  background:
    linear-gradient(
      135deg,
      color-mix(in srgb, var(--text) 9%, transparent),
      transparent 42%,
      color-mix(in srgb, var(--blue) 5%, transparent)
    ),
    color-mix(in srgb, var(--acrylic) 64%, transparent);
  background-clip: padding-box;
  pointer-events: none;
  backdrop-filter: blur(38px) saturate(175%);
  -webkit-backdrop-filter: blur(38px) saturate(175%);
}

.site-header__inner > * {
  position: relative;
  z-index: 1;
}

.site-nav {
  display: flex;
  gap: clamp(1.6rem, 3.2vw, 3.5rem);
}

.site-nav a {
  position: relative;
  display: inline-flex;
  align-items: center;
  min-height: 2.75rem;
  padding: 0.5rem 0;
  color: var(--text-soft);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
}

.site-nav a::after {
  position: absolute;
  right: 0;
  bottom: 0.15rem;
  left: 0;
  height: 2px;
  content: '';
  background: var(--coral);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 220ms var(--ease-out);
}

.site-nav a:hover,
.site-nav a:focus-visible {
  color: var(--text);
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
  gap: 0.65rem;
}

.menu-toggle {
  display: none;
  width: 3rem;
  height: 3rem;
  padding: 0.7rem;
  border: 1px solid var(--line-strong);
  border-radius: 0.65rem 0.65rem 0.48rem 0.48rem;
  background: color-mix(in srgb, var(--acrylic) 68%, transparent);
  transition:
    transform 220ms var(--ease-out),
    background-color 220ms ease;
}

.menu-toggle:hover,
.menu-toggle:focus-visible {
  background: color-mix(in srgb, var(--acrylic-strong) 82%, transparent);
  transform: rotate(1.5deg);
}

.menu-toggle span {
  display: block;
  height: 1.5px;
  margin-block: 0.3rem;
  background: currentColor;
}

@media (max-width: 860px) {
  .site-header {
    top: 0.55rem;
  }

  .site-header__inner {
    grid-template-columns: 1fr auto;
    min-height: calc(var(--header) - 0.7rem);
    padding-inline: 0.75rem;
  }

  .menu-toggle {
    display: block;
  }

  .site-nav {
    position: absolute;
    top: calc(100% + 0.55rem);
    right: 0;
    left: 0;
    display: grid;
    gap: 0;
    padding: 0.55rem 0.65rem 0.7rem;
    overflow: hidden;
    border: 1px solid color-mix(in srgb, var(--line-strong) 72%, transparent);
    border-radius: 0.9rem 0.9rem 1.15rem 1.15rem;
    background:
      linear-gradient(
        145deg,
        color-mix(in srgb, var(--text) 8%, transparent),
        transparent 46%,
        color-mix(in srgb, var(--blue) 5%, transparent)
      ),
      color-mix(in srgb, var(--acrylic-strong) 62%, transparent);
    background-clip: padding-box;
    box-shadow:
      0 1.4rem 3.8rem rgb(8 9 13 / 0.22),
      inset 0 1px 0 color-mix(in srgb, var(--text) 8%, transparent);
    visibility: hidden;
    opacity: 0;
    pointer-events: none;
    transform: translateY(-0.65rem) scale(0.985);
    transform-origin: 50% 0;
    transition:
      opacity 220ms ease,
      transform 260ms var(--ease-out),
      visibility 220ms;
    backdrop-filter: blur(42px) saturate(185%);
    -webkit-backdrop-filter: blur(42px) saturate(185%);
  }

  .site-nav--open {
    visibility: visible;
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0) scale(1);
  }

  .site-nav a {
    min-height: 3.35rem;
    padding: 0.9rem 0.85rem;
    border-bottom: 1px solid var(--line);
    border-radius: 0.55rem;
    color: var(--text);
    font-size: 1rem;
    transition:
      padding-left 220ms var(--ease-out),
      background-color 220ms ease;
  }

  .site-nav a:last-child {
    border-bottom: 0;
  }

  .site-nav a::after {
    display: none;
  }

  .site-nav a:hover,
  .site-nav a:focus-visible {
    padding-left: 1.15rem;
    background: color-mix(in srgb, var(--text) 6%, transparent);
  }
}

@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .site-header__inner::before {
    background: color-mix(in srgb, var(--acrylic-strong) 92%, transparent);
  }

  .site-nav {
    background: color-mix(in srgb, var(--acrylic-strong) 96%, transparent);
  }
}

@media (prefers-reduced-motion: reduce) {
  .site-nav,
  .site-nav a,
  .menu-toggle {
    transition: none;
  }
}
</style>
