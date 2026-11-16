import { readonly, ref } from 'vue'

export type Theme = 'light' | 'dark'

const theme = ref<Theme>('dark')
let initialized = false

function applyTheme(nextTheme: Theme) {
  theme.value = nextTheme
  document.documentElement.dataset.theme = nextTheme
  document.documentElement.style.colorScheme = nextTheme
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', nextTheme === 'dark' ? '#08090d' : '#ffffff')
}

export function initTheme() {
  if (initialized) return
  initialized = true
  const stored = window.localStorage.getItem('radar-theme')
  const preferred = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
  applyTheme(stored === 'light' || stored === 'dark' ? stored : preferred)
}

export function useTheme() {
  function toggleTheme() {
    const nextTheme: Theme = theme.value === 'dark' ? 'light' : 'dark'
    applyTheme(nextTheme)
    window.localStorage.setItem('radar-theme', nextTheme)
  }

  return { theme: readonly(theme), toggleTheme }
}
