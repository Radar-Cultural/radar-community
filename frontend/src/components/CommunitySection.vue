<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'
import communityImage from '../assets/community-workshop.webp'
import booksImage from '../assets/fragment-books.webp'
import cinemaImage from '../assets/fragment-cinema.webp'
import danceImage from '../assets/fragment-dance.webp'
import musicImage from '../assets/fragment-music.webp'
import AsyncAction from './AsyncAction.vue'

const slides = [
  { src: communityImage, label: 'Creación compartida', position: 'center 58%' },
  { src: danceImage, label: 'Danza', position: 'center' },
  { src: musicImage, label: 'Música', position: 'center' },
  { src: cinemaImage, label: 'Cine', position: 'center' },
  { src: booksImage, label: 'Lectura', position: 'center' },
] as const

const root = ref<HTMLElement | null>(null)
let context: gsap.Context | undefined
let media: gsap.MatchMedia | undefined

onMounted(() => {
  if (!root.value || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  context = gsap.context(() => {
    media = gsap.matchMedia()

    const prepareCarousel = () => {
      gsap.set('.community__slide', { opacity: 0, scale: 1.08 })
      gsap.set('.community__slide:first-child', { opacity: 1, scale: 1 })
      gsap.set('.community__label', { opacity: 0, yPercent: 55 })
      gsap.set('.community__label:first-child', { opacity: 1, yPercent: 0 })
      gsap.set('.community__more', { opacity: 0, y: 18 })
      gsap.set('.community__progress', { scaleX: 0 })
    }

    const addCarouselSequence = (timeline: gsap.core.Timeline) => {
      const step = 0.18

      slides.slice(1).forEach((_, offset) => {
        const current = offset + 1
        const previous = current
        const next = current + 1
        const at = 0.2 + offset * step

        timeline
          .to(
            `.community__slide:nth-child(${previous})`,
            { opacity: 0, scale: 0.95, duration: 0.09, ease: 'power2.in' },
            at,
          )
          .fromTo(
            `.community__slide:nth-child(${next})`,
            { opacity: 0, scale: 1.08 },
            { opacity: 1, scale: 1, duration: 0.11, ease: 'power2.out' },
            at + 0.06,
          )
          .to(
            `.community__label:nth-child(${previous})`,
            { opacity: 0, yPercent: -55, duration: 0.07, ease: 'power2.in' },
            at,
          )
          .fromTo(
            `.community__label:nth-child(${next})`,
            { opacity: 0, yPercent: 55 },
            { opacity: 1, yPercent: 0, duration: 0.1, ease: 'power2.out' },
            at + 0.06,
          )
      })

      timeline
        .to('.community__sweep', { rotate: 540, duration: 0.92, ease: 'none' }, 0.08)
        .to('.community__progress', { scaleX: 1, duration: 0.86, ease: 'none' }, 0.1)
        .to('.community__more', { opacity: 1, y: 0, duration: 0.1, ease: 'power2.out' }, 0.84)
    }

    media.add('(min-width: 821px)', () => {
      prepareCarousel()

      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: '.community__stage',
          start: 'top top',
          end: '+=1750',
          pin: true,
          scrub: 0.72,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      })

      timeline.fromTo(
        '.community__carousel',
        { opacity: 0.5, scale: 0.84, rotate: -4 },
        { opacity: 1, scale: 1, rotate: 0, duration: 0.18, ease: 'power2.out' },
        0,
      )
      addCarouselSequence(timeline)
      timeline.fromTo(
        '.community__actions',
        { opacity: 0, y: 18 },
        { opacity: 1, y: 0, duration: 0.12, ease: 'power2.out' },
        0.86,
      )
    })

    media.add('(max-width: 820px)', () => {
      prepareCarousel()

      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: '.community__visual',
          start: 'top 18%',
          end: '+=1250',
          pin: true,
          scrub: 0.65,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      })

      timeline.fromTo(
        '.community__carousel',
        { opacity: 0.55, scale: 0.86 },
        { opacity: 1, scale: 1, duration: 0.16, ease: 'power2.out' },
        0,
      )
      addCarouselSequence(timeline)

      gsap.from('.community__actions', {
        opacity: 0,
        y: 20,
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: { trigger: '.community__actions', start: 'top 88%' },
      })
    })
  }, root.value)
})

onUnmounted(() => {
  media?.revert()
  context?.revert()
})
</script>

<template>
  <section id="comunidad" ref="root" class="community" aria-labelledby="community-title">
    <div class="community__stage page-width">
      <header class="community__heading">
        <p>Código abierto · colaboración</p>
        <div>
          <h2 id="community-title" class="community__title display-title">
            La señal crece cuando <i>se comparte.</i>
          </h2>
        </div>
      </header>

      <div class="community__visual">
        <div class="community__caption" aria-live="off">
          <p>Muchas expresiones.<br /><strong>Más formas de encontrarlas.</strong></p>

          <div class="community__labels" aria-hidden="true">
            <span v-for="slide in slides" :key="slide.label" class="community__label">
              {{ slide.label }}
            </span>
          </div>

          <div class="community__meter" aria-hidden="true">
            <span>Señales compartidas</span>
            <i><b class="community__progress"></b></i>
            <span>{{ String(slides.length).padStart(2, '0') }}</span>
          </div>
        </div>

        <div
          class="community__carousel"
          role="img"
          aria-label="Un radar recorre escenas de creación compartida, danza, música, cine y lectura"
        >
          <span class="community__orbit community__orbit--outer" aria-hidden="true"></span>
          <span class="community__orbit community__orbit--inner" aria-hidden="true"></span>

          <div class="community__slides" aria-hidden="true">
            <img
              v-for="slide in slides"
              :key="slide.src"
              class="community__slide"
              :src="slide.src"
              :style="{ objectPosition: slide.position }"
              alt=""
              width="1384"
              height="1384"
              loading="lazy"
              decoding="async"
            />
          </div>

          <span class="community__sweep" aria-hidden="true"></span>
          <span class="community__centre" aria-hidden="true"></span>
          <span class="community__more" aria-hidden="true">y más…</span>
        </div>
      </div>

      <div class="community__footer">
        <div class="community__actions">
          <AsyncAction
            href="https://github.com/Radar-Cultural/radar-community/blob/main/CONTRIBUTING.md"
            label="Conocer la comunidad"
            external
          >
            Conocer la comunidad
          </AsyncAction>
          <AsyncAction
            href="https://github.com/Radar-Cultural/radar-community"
            label="Explorar el código"
            variant="text"
            external
          >
            Explorar el código
          </AsyncAction>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.community {
  --community-accent: var(--blue-bright);

  position: relative;
  overflow: clip;
  color: var(--text);
  background: var(--canvas);
  transition:
    color 500ms var(--ease-out),
    background-color 500ms var(--ease-out);
}
.community__stage {
  position: relative;
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100svh;
  padding-block: calc(var(--header) + 1.75rem) 1.5rem;
}
.community__heading {
  position: relative;
  z-index: 3;
  display: grid;
  grid-template-columns: minmax(12rem, 0.28fr) minmax(0, 1fr);
  gap: clamp(2rem, 6vw, 7rem);
  align-items: start;
}
.community__heading > p {
  margin: 0.45rem 0 0;
  color: var(--text-soft);
  font-size: 0.6rem;
  font-weight: 750;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.community__title {
  max-width: 13ch;
  font-size: clamp(3.25rem, 5.2vw, 5.8rem);
  line-height: 0.88;
}
.community__title i {
  color: var(--wine);
  font-style: normal;
}
.community__visual {
  position: relative;
  min-height: clamp(30rem, 58vh, 38rem);
}
.community__caption {
  position: absolute;
  z-index: 3;
  top: 51%;
  left: 0;
  width: min(27vw, 22rem);
  transform: translateY(-50%);
}
.community__caption > p {
  margin: 0;
  color: var(--text-soft);
  font-size: clamp(1.15rem, 1.65vw, 1.65rem);
  line-height: 1.2;
}
.community__caption > p strong {
  color: var(--text);
  font-family: var(--display);
  font-size: 1.22em;
  font-weight: 650;
  letter-spacing: -0.04em;
}
.community__labels {
  position: relative;
  height: clamp(6.5rem, 8.5vw, 8rem);
  margin-top: 1.5rem;
  overflow: hidden;
}
.community__label {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  color: var(--community-accent);
  font-family: var(--display);
  font-size: clamp(2.4rem, 3.8vw, 4rem);
  font-weight: 650;
  line-height: 0.9;
  letter-spacing: -0.065em;
  will-change: transform, opacity;
}
.community__meter {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.8rem;
  align-items: center;
  color: var(--text-soft);
  font-size: 0.58rem;
  font-weight: 750;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}
.community__meter i {
  position: relative;
  display: block;
  height: 1px;
  background: var(--line);
}
.community__meter b {
  position: absolute;
  inset: 0;
  display: block;
  background: var(--coral);
  transform-origin: left center;
  will-change: transform;
}
.community__carousel {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 66%;
  width: clamp(28rem, 40vw, 36rem);
  aspect-ratio: 1;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  will-change: transform, opacity;
}
.community__slides {
  position: absolute;
  z-index: 1;
  inset: 0;
  overflow: hidden;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: var(--surface);
  box-shadow: var(--shadow);
}
.community__slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  will-change: transform, opacity;
}
.community__orbit {
  position: absolute;
  z-index: 0;
  border: 1px solid var(--line);
  border-radius: 50%;
  pointer-events: none;
}
.community__orbit--outer {
  inset: -6%;
  border-color: color-mix(in srgb, var(--community-accent) 42%, var(--line));
  border-right-color: transparent;
}
.community__orbit--inner {
  inset: 28%;
  z-index: 2;
  border-color: rgb(247 248 250 / 0.52);
}
.community__sweep {
  position: absolute;
  z-index: 3;
  top: 50%;
  left: 50%;
  display: block;
  width: 48%;
  height: 48%;
  border-left: 1px solid color-mix(in srgb, var(--coral) 84%, #fff);
  background: conic-gradient(
    from 252deg at 0 0,
    transparent 0deg,
    color-mix(in srgb, var(--coral) 28%, transparent) 34deg,
    transparent 37deg
  );
  filter: drop-shadow(0 0 0.65rem rgb(8 9 13 / 0.35));
  transform-origin: 0 0;
  will-change: transform;
}
.community__centre {
  position: absolute;
  z-index: 4;
  top: 50%;
  left: 50%;
  width: 0.46rem;
  height: 0.46rem;
  border-radius: 50%;
  background: var(--coral);
  box-shadow: 0 0 0 0.38rem rgb(255 90 79 / 0.22);
  transform: translate(-50%, -50%);
}
.community__more {
  position: absolute;
  z-index: 5;
  right: 11%;
  bottom: 12%;
  color: #fff;
  font-family: var(--display);
  font-size: clamp(2rem, 3.2vw, 3.2rem);
  font-weight: 650;
  line-height: 0.9;
  letter-spacing: -0.055em;
  text-shadow: 0 0.12rem 1.25rem rgb(8 9 13 / 0.72);
  will-change: transform, opacity;
}
.community__footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.75rem;
}
.community__actions {
  display: flex;
  gap: 1rem;
  will-change: transform, opacity;
}

:global(:root[data-theme='light']) .community {
  --community-accent: var(--blue);
}

@media (max-width: 820px) {
  .community__stage {
    display: block;
    min-height: auto;
    padding-block: calc(var(--header) + 4rem) 4rem;
  }
  .community__heading {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .community__heading > p {
    margin: 0;
  }
  .community__title {
    max-width: 11ch;
    font-size: clamp(3.3rem, 12vw, 5.8rem);
  }
  .community__visual {
    min-height: 46rem;
    margin-top: 1.5rem;
  }
  .community__carousel {
    top: 39%;
    left: 50%;
    width: clamp(22rem, 82vw, 31rem);
  }
  .community__caption {
    top: auto;
    right: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    transform: none;
  }
  .community__labels {
    height: 6.25rem;
    margin-top: 1rem;
  }
  .community__label {
    justify-content: center;
    font-size: clamp(2.5rem, 9vw, 4rem);
  }
  .community__meter {
    max-width: 30rem;
    margin-inline: auto;
  }
  .community__footer {
    display: grid;
    padding-top: 2rem;
  }
  .community__actions {
    display: grid;
  }
  .community__actions :deep(.action) {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 430px) {
  .community__title {
    max-width: 100%;
    font-size: clamp(3rem, 14.2vw, 3.8rem);
  }
  .community__visual {
    min-height: 39rem;
  }
  .community__carousel {
    top: 36%;
    width: min(87vw, 23rem);
  }
  .community__caption > p {
    font-size: 1rem;
  }
  .community__meter {
    gap: 0.55rem;
    font-size: 0.52rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .community__slide,
  .community__label,
  .community__more {
    opacity: 0;
    transform: none;
  }
  .community__slide:first-child,
  .community__label:first-child,
  .community__more,
  .community__actions,
  .community__carousel {
    opacity: 1;
    transform: none;
  }
  .community__carousel {
    transform: translate(-50%, -50%);
  }
  .community__progress {
    transform: scaleX(1);
  }
}
</style>
