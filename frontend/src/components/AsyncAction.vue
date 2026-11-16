<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    href: string
    variant?: 'primary' | 'text'
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
  }, 380)
}
</script>

<template>
  <a
    class="action"
    :class="['action--' + variant, { 'is-busy': busy }]"
    :href="href"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noreferrer' : undefined"
    :aria-busy="busy"
    @click="activate"
  >
    <span><slot /></span>
    <span v-if="busy" class="action__loader" aria-hidden="true"></span>
    <svg v-else viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h13M13 6l6 6-6 6" />
    </svg>
  </a>
</template>

<style scoped>
.action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.85rem;
  min-height: 3.7rem;
  padding: 0.95rem 1.55rem;
  border: 1px solid transparent;
  border-radius: 0.2rem;
  font-size: 0.96rem;
  font-weight: 730;
  line-height: 1;
  text-decoration: none;
  transition:
    transform 220ms var(--ease-bounce),
    box-shadow 220ms ease,
    color 180ms ease;
}

.action--primary {
  color: #fff;
  background: var(--blue);
  box-shadow: 0 0.85rem 2.4rem rgb(49 87 255 / 0.24);
}

.action--text {
  min-height: 3.7rem;
  padding: 0.95rem 1.3rem;
  border-color: var(--line-strong);
  border-radius: 0.2rem;
  color: inherit;
  background: color-mix(in srgb, var(--acrylic) 82%, transparent);
  box-shadow: 0 0.75rem 2.2rem rgb(8 9 13 / 0.08);
  backdrop-filter: blur(16px) saturate(135%);
  -webkit-backdrop-filter: blur(16px) saturate(135%);
}

.action:hover {
  transform: translateY(-0.22rem);
}

.action--primary:hover {
  box-shadow: 0 1.1rem 2.8rem rgb(49 87 255 / 0.34);
}

.action svg {
  width: 1.2rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: square;
  stroke-linejoin: miter;
  stroke-width: 1.8;
  transition: transform 180ms var(--ease-out);
}

.action:hover svg {
  transform: translateX(0.25rem);
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
  .action--primary {
    width: 100%;
  }
}
</style>
