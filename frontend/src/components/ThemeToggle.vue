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
    type="button"
    :aria-label="label"
    :title="label"
    @click="toggleTheme"
  >
    <span class="theme-toggle__track" aria-hidden="true">
      <svg class="theme-toggle__moon" viewBox="0 0 24 24">
        <path d="M19 15.2A7.5 7.5 0 0 1 8.8 5 7.7 7.7 0 1 0 19 15.2Z" />
      </svg>
      <svg class="theme-toggle__sun" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="3.2" />
        <path
          d="M12 2.2v2.2M12 19.6v2.2M2.2 12h2.2M19.6 12h2.2M5.1 5.1l1.6 1.6M17.3 17.3l1.6 1.6M18.9 5.1l-1.6 1.6M6.7 17.3l-1.6 1.6"
        />
      </svg>
      <span class="theme-toggle__thumb"></span>
    </span>
  </button>
</template>

<style scoped>
.theme-toggle {
  display: grid;
  padding: 0;
  border: 0;
  color: var(--color-text);
  background: transparent;
  cursor: pointer;
}

.theme-toggle__track {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 4.35rem;
  height: 2.25rem;
  padding: 0.35rem;
  border: 1px solid var(--color-line-strong);
  border-radius: 999px;
  background: var(--color-acrylic);
  box-shadow: inset 0 1px rgb(255 255 255 / 0.09);
  backdrop-filter: blur(14px);
}

.theme-toggle svg {
  z-index: 1;
  align-self: center;
  justify-self: center;
  width: 1rem;
  height: 1rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-width: 1.65;
}

.theme-toggle__moon {
  color: #fff;
}

.theme-toggle__sun {
  color: var(--color-gold);
}

.theme-toggle__thumb {
  position: absolute;
  top: 0.28rem;
  left: 0.28rem;
  width: 1.57rem;
  height: 1.57rem;
  border-radius: 50%;
  background: linear-gradient(145deg, #8369ff, var(--color-violet));
  box-shadow: 0 0.35rem 1rem rgb(109 74 255 / 0.36);
  transition: transform 260ms var(--ease-out);
}

:global(html[data-theme='light'] .theme-toggle__thumb) {
  transform: translateX(2.08rem);
  background: #fff;
  box-shadow: 0 0.3rem 0.9rem rgb(13 19 33 / 0.16);
}

.theme-toggle:focus-visible {
  outline: 2px solid var(--color-violet);
  outline-offset: 0.3rem;
  border-radius: 999px;
}
</style>
