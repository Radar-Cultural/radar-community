<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    href: string
    variant?: 'primary' | 'secondary'
    external?: boolean
  }>(),
  { variant: 'primary', external: false },
)

const busy = ref(false)

function activate(event: MouseEvent) {
  if (props.external || !props.href.startsWith('#') || busy.value) return
  event.preventDefault()
  busy.value = true
  window.setTimeout(() => {
    document.querySelector(props.href)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    window.history.replaceState(null, '', props.href)
    busy.value = false
  }, 420)
}
</script>

<template>
  <a
    class="action"
    :class="`action--${variant}`"
    :href="href"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noreferrer' : undefined"
    :aria-busy="busy"
    @click="activate"
  >
    <span class="action__label"><slot /></span>
    <span v-if="busy" class="action__loader" aria-hidden="true"></span>
    <svg v-else class="action__arrow" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h13M13 6l6 6-6 6" />
    </svg>
  </a>
</template>

<style scoped>
.action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  min-height: 3.7rem;
  padding: 0.9rem 1.55rem;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 0.98rem;
  font-weight: 720;
  line-height: 1;
  text-decoration: none;
  transition:
    transform 220ms var(--ease-bounce),
    box-shadow 220ms ease,
    background 220ms ease;
}

.action--primary {
  color: #fff;
  background: linear-gradient(120deg, #5836f4, #794cff 60%, #6544f2);
  box-shadow: 0 0.8rem 2.2rem rgb(109 74 255 / 0.25);
}

.action--secondary {
  border-color: var(--color-line-strong);
  color: var(--color-text);
  background: var(--color-acrylic);
  backdrop-filter: blur(16px);
}

.action:hover {
  transform: translateY(-0.22rem) scale(1.015);
}

.action--primary:hover {
  box-shadow: 0 1rem 2.8rem rgb(109 74 255 / 0.38);
}

.action:focus-visible {
  outline: 2px solid var(--color-jade);
  outline-offset: 0.25rem;
}

.action__arrow {
  width: 1.2rem;
  height: 1.2rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
  transition: transform 200ms var(--ease-out);
}

.action:hover .action__arrow {
  transform: translateX(0.2rem);
}

.action__loader {
  width: 1.05rem;
  aspect-ratio: 1;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: action-spin 650ms linear infinite;
}

@keyframes action-spin {
  to {
    transform: rotate(1turn);
  }
}

@media (max-width: 520px) {
  .action {
    width: 100%;
  }
}
</style>
