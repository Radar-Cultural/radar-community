<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from '../composables/useTheme'

const { theme, toggleTheme } = useTheme()
const label = computed(() =>
  theme.value === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro',
)
</script>

<template>
  <button
    class="theme-toggle"
    :class="{ 'is-light': theme === 'light' }"
    type="button"
    :aria-label="label"
    :title="label"
    @click="toggleTheme"
  >
    <span class="theme-toggle__track" aria-hidden="true">
      <svg class="theme-toggle__icon theme-toggle__icon--moon" viewBox="0 0 24 24">
        <path d="M19 15.2A7.5 7.5 0 0 1 8.8 5 7.7 7.7 0 1 0 19 15.2Z" />
      </svg>
      <svg class="theme-toggle__icon theme-toggle__icon--sun" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="3.4" />
        <path
          d="M12 2.4v2.2M12 19.4v2.2M4.6 12H2.4M21.6 12h-2.2M5.2 5.2l1.55 1.55M17.25 17.25l1.55 1.55M18.8 5.2l-1.55 1.55M6.75 17.25 5.2 18.8"
        />
      </svg>
      <span class="theme-toggle__thumb"></span>
    </span>
  </button>
</template>

<style scoped>
.theme-toggle {
  display: grid;
  place-items: center;
  justify-self: start;
  min-width: 2.75rem;
  min-height: 2.75rem;
  padding: 0.3rem;
  border: 0;
  border-radius: 999px;
  color: inherit;
  background: transparent;
  transition: transform 220ms var(--ease-out);
}

.theme-toggle:hover {
  transform: rotate(-2deg);
}

.theme-toggle__track {
  position: relative;
  display: grid;
  place-items: center start;
  width: 3.55rem;
  height: 2rem;
  padding: 0.32rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: var(--acrylic);
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--text) 3%, transparent);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.theme-toggle__icon {
  position: absolute;
  z-index: 1;
  top: 50%;
  width: 0.86rem;
  height: 0.86rem;
  color: var(--text);
  transform: translateY(-50%);
  transition:
    opacity 220ms ease,
    color 220ms ease;
}

.theme-toggle__icon--moon {
  left: 0.57rem;
  fill: currentColor;
  opacity: 0.92;
}

.theme-toggle__icon--sun {
  right: 0.52rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-width: 1.8;
  opacity: 0.12;
}

.theme-toggle__thumb {
  position: absolute;
  z-index: 2;
  top: 0.27rem;
  right: 0.27rem;
  width: 1.4rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: 0 0.24rem 0.7rem rgb(8 9 13 / 0.2);
  transition:
    transform 260ms var(--ease-out),
    background-color 260ms ease;
}

.theme-toggle.is-light .theme-toggle__thumb {
  transform: translateX(-1.52rem);
  background: var(--wine);
}

.theme-toggle.is-light .theme-toggle__icon--moon {
  opacity: 0.12;
}

.theme-toggle.is-light .theme-toggle__icon--sun {
  color: var(--ink);
  opacity: 0.9;
}

@media (prefers-reduced-motion: reduce) {
  .theme-toggle,
  .theme-toggle__icon,
  .theme-toggle__thumb {
    transition: none;
  }
}
</style>
