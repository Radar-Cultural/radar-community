<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'
import AsyncAction from './AsyncAction.vue'
import RadarScene from './RadarScene.vue'
import { listEvents, type CulturalEvent } from '../api/radar'

const root = ref<HTMLElement | null>(null)
const featuredEvents = ref<CulturalEvent[]>([])
const eventsRequest = new AbortController()
let context: gsap.Context | undefined
let media: gsap.MatchMedia | undefined
const scatter = [
  { x: -34, y: 62, rotation: -15 },
  { x: 26, y: 68, rotation: 12 },
  { x: -24, y: 56, rotation: -8 },
  { x: 34, y: 58, rotation: 14 },
]

onMounted(() => {
  const query = {
    not_finished_at: new Date().toISOString(),
    status: 'EventScheduled' as const,
    has_image: true,
    page_size: 12,
  }
  void listEvents(query, eventsRequest.signal)
    .then(async (firstPage) => {
      if (!firstPage.count) return
      const pageCount = Math.ceil(firstPage.count / query.page_size)
      const randomPage = Math.floor(Math.random() * pageCount) + 1
      const page =
        randomPage === 1
          ? firstPage
          : await listEvents({ ...query, page: randomPage }, eventsRequest.signal)
      const candidates = [...page.results]
      if (candidates.length < 4) {
        const selectedIds = new Set(candidates.map((event) => event.id))
        candidates.push(...firstPage.results.filter((event) => !selectedIds.has(event.id)))
      }
      for (let index = candidates.length - 1; index > 0; index -= 1) {
        const randomIndex = Math.floor(Math.random() * (index + 1))
        ;[candidates[index], candidates[randomIndex]] = [
          candidates[randomIndex]!,
          candidates[index]!,
        ]
      }
      featuredEvents.value = candidates.slice(0, 4)
    })
    .catch(() => {
      // La agenda informa el error; el hero conserva sus imágenes editoriales.
    })
  if (!root.value || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  context = gsap.context(() => {
    const fragments = gsap.utils.toArray<HTMLElement>('.fragment-slot')
    const fragmentFrames = gsap.utils.toArray<HTMLElement>('.fragment-frame')
    gsap
      .timeline({ defaults: { ease: 'power4.out' }, delay: 0.08 })
      .from('.hero__brand-word', { yPercent: 110, duration: 0.72, stagger: 0.05 })
      .from('.hero__phrase, .hero__actions', { autoAlpha: 0, y: 18, duration: 0.45 }, '-=0.38')
      .from(
        fragmentFrames,
        { autoAlpha: 0, y: -64, scale: 0.94, duration: 0.8, stagger: 0.065 },
        0.14,
      )

    media = gsap.matchMedia()
    media.add('(min-width: 801px)', () => {
      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: root.value,
          start: 'top top',
          end: '+=150%',
          pin: true,
          scrub: 0.85,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      })
      fragments.forEach((fragment, index) => {
        const movement = scatter[index]!
        timeline.fromTo(
          fragment,
          { x: 0, y: 0, rotation: 0, scale: 1, opacity: 1, filter: 'blur(0px)' },
          {
            x: `${movement.x}vw`,
            y: `${movement.y}vh`,
            rotation: movement.rotation,
            scale: 0.78,
            opacity: 0,
            filter: 'blur(18px)',
            duration: 0.88,
            ease: 'none',
          },
          0,
        )
      })
      timeline.to(
        '.hero__copy',
        {
          yPercent: 18,
          scale: 0.94,
          opacity: 0,
          filter: 'blur(10px)',
          duration: 0.72,
          ease: 'none',
        },
        0.12,
      )
      timeline.fromTo(
        '.hero__handoff',
        { opacity: 0 },
        { opacity: 1, duration: 0.22, ease: 'none' },
        0.78,
      )
      timeline.to('.hero__scroll', { opacity: 0, duration: 0.2, ease: 'none' }, 0.28)
    })
    media.add('(max-width: 800px)', () => {
      gsap.fromTo(
        fragments,
        { y: 0, opacity: 1, filter: 'blur(0px)' },
        {
          y: 140,
          opacity: 0,
          filter: 'blur(10px)',
          stagger: 0.025,
          ease: 'none',
          scrollTrigger: {
            trigger: root.value,
            start: '18% top',
            end: '85% top',
            scrub: 0.65,
            invalidateOnRefresh: true,
          },
        },
      )
      gsap.fromTo(
        '.hero__handoff',
        { opacity: 0 },
        {
          opacity: 1,
          ease: 'none',
          scrollTrigger: {
            trigger: root.value,
            start: '65% top',
            end: 'bottom top',
            scrub: true,
          },
        },
      )
    })
  }, root.value)
})
onUnmounted(() => {
  eventsRequest.abort()
  media?.revert()
  context?.revert()
})
</script>

<template>
  <section ref="root" class="hero" aria-labelledby="hero-title">
    <div class="hero__handoff" aria-hidden="true"></div>
    <div class="hero__inner page-width">
      <div class="hero__copy">
        <h1 id="hero-title" class="hero__brand display-title" aria-label="Radar Cultural">
          <span><i class="hero__brand-word">Radar</i></span>
          <span><i class="hero__brand-word">Cultural</i></span>
        </h1>
        <p class="hero__phrase">La cultura sucede. Que nadie se la pierda.</p>
        <div class="hero__actions">
          <AsyncAction href="/agenda/">Ver agenda completa</AsyncAction>
          <AsyncAction href="#proyecto" variant="text">Ver cómo funciona</AsyncAction>
        </div>
      </div>
    </div>
    <RadarScene :events="featuredEvents" />
    <p class="hero__scroll" aria-hidden="true"><span></span> Sigue la señal</p>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 100svh;
  overflow: hidden;
  color: var(--text);
  background: var(--canvas);
  transition:
    color 500ms var(--ease-out),
    background-color 500ms var(--ease-out);
}
.hero__inner {
  position: relative;
  z-index: 3;
  display: grid;
  place-items: center;
  min-height: 100svh;
  padding-block: calc(var(--header) + 2rem) 4rem;
  pointer-events: none;
}
.hero__handoff {
  position: absolute;
  z-index: 2;
  right: 0;
  bottom: -1px;
  left: 0;
  height: clamp(6rem, 18vh, 12rem);
  border-top: 1px solid color-mix(in srgb, var(--text) 8%, transparent);
  background: color-mix(in srgb, var(--canvas) 72%, transparent);
  box-shadow: 0 -3rem 6rem color-mix(in srgb, var(--canvas) 78%, transparent);
  backdrop-filter: blur(20px) saturate(125%);
  -webkit-backdrop-filter: blur(20px) saturate(125%);
  pointer-events: none;
}
.hero__copy {
  display: grid;
  justify-items: center;
  width: min(58rem, 68vw);
  text-align: center;
  pointer-events: auto;
  will-change: transform, filter, opacity;
}
.hero__brand {
  display: grid;
  font-size: clamp(5rem, 9.6vw, 10.4rem);
  line-height: 0.76;
  letter-spacing: -0.085em;
}
.hero__brand > span {
  display: block;
  overflow: hidden;
  padding: 0 0.06em 0.12em;
}
.hero__brand-word {
  display: block;
  font-style: normal;
}
.hero__phrase {
  margin: 1.7rem 0 0;
  font-size: clamp(1.2rem, 1.9vw, 1.7rem);
  line-height: 1.35;
  text-wrap: balance;
}
.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem 2.1rem;
  justify-content: center;
  margin-top: 2rem;
}
.hero__scroll {
  position: absolute;
  z-index: 4;
  right: var(--gutter);
  bottom: 1.5rem;
  display: flex;
  gap: 0.6rem;
  align-items: center;
  margin: 0;
  color: var(--text-soft);
  font-size: 0.76rem;
  font-weight: 650;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}
.hero__scroll span {
  display: block;
  width: 2.5rem;
  height: 1px;
  background: var(--text);
  transform-origin: right;
  animation: scroll-pulse 1.8s ease-in-out infinite;
}
@keyframes scroll-pulse {
  0%,
  100% {
    transform: scaleX(0.4);
  }
  50% {
    transform: scaleX(1);
  }
}
@media (max-width: 800px) {
  .hero__inner {
    padding-bottom: 3rem;
  }
  .hero__copy {
    width: min(100%, 31rem);
  }
  .hero__brand {
    font-size: clamp(4.25rem, 21.5vw, 7.2rem);
  }
  .hero__phrase {
    max-width: 25rem;
    margin-top: 1.2rem;
    font-size: 1.06rem;
  }
  .hero__actions {
    display: grid;
    width: min(100%, 22rem);
    gap: 0.65rem;
    margin-top: 1.4rem;
  }
  .hero__actions :deep(.action) {
    width: 100%;
    justify-content: space-between;
  }
  .hero__actions :deep(.action--text) {
    border: 1px solid var(--line-strong);
  }
  .hero__scroll {
    display: none;
  }
}
@media (prefers-reduced-motion: reduce) {
  .hero__scroll span {
    animation: none;
  }
}
</style>
