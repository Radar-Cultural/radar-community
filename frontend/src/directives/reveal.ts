import type { Directive } from 'vue'

export const reveal: Directive<HTMLElement> = {
  mounted(element) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      element.dataset.revealed = 'true'
      return
    }

    element.dataset.reveal = 'pending'
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return
        element.dataset.revealed = 'true'
        observer.disconnect()
      },
      { rootMargin: '0px 0px -12% 0px', threshold: 0.12 },
    )
    observer.observe(element)
  },
}
