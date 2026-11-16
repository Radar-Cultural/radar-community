<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'

const fields = ['Qué', 'Dónde', 'Cuándo', 'Acceso'] as const
const uses = ['Descubrir', 'Compartir', 'Reutilizar'] as const

const root = ref<HTMLElement | null>(null)
let context: gsap.Context | undefined
let media: gsap.MatchMedia | undefined

onMounted(() => {
  if (!root.value || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  context = gsap.context(() => {
    media = gsap.matchMedia()

    media.add('(min-width: 821px)', () => {
      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: '.data__stage',
          start: 'top top',
          end: '+=1450',
          pin: true,
          scrub: 0.75,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      })

      timeline
        .fromTo(
          '.data__radar',
          { scale: 0.62, opacity: 0.25 },
          { scale: 1, opacity: 1, duration: 0.72, ease: 'none' },
          0,
        )
        .fromTo(
          '.data__title',
          { '--title-reveal': '0%' },
          { '--title-reveal': '100%', duration: 0.82, ease: 'none' },
          0.08,
        )
        .to('.data__radar-sweep', { rotate: 212, duration: 1, ease: 'none' }, 0)
        .to('.data__radar-ring--broken', { rotate: -52, duration: 1, ease: 'none' }, 0)
        .fromTo(
          '.data__radar-signal',
          { opacity: 0, scale: 0 },
          { opacity: 1, scale: 1, duration: 0.12, stagger: 0.11, ease: 'back.out(1.8)' },
          0.28,
        )
        .fromTo(
          '.data__use',
          { opacity: 0, y: 18 },
          { opacity: 1, y: 0, duration: 0.2, stagger: 0.1, ease: 'power2.out' },
          0.62,
        )
        .to('.data__stream--top', { xPercent: -9, duration: 1, ease: 'none' }, 0)
        .to('.data__stream--bottom', { xPercent: 9, duration: 1, ease: 'none' }, 0)
    })

    media.add('(max-width: 820px)', () => {
      gsap.from('.data__radar', {
        opacity: 0,
        scale: 0.72,
        duration: 1.05,
        ease: 'power3.out',
        scrollTrigger: { trigger: root.value, start: 'top 68%' },
      })
      gsap.from('.data__radar-signal, .data__use', {
        opacity: 0,
        scale: 0.7,
        stagger: 0.08,
        duration: 0.65,
        ease: 'power3.out',
        scrollTrigger: { trigger: '.data__title', start: 'top 70%' },
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
  <section id="datos" ref="root" class="data" aria-labelledby="data-title">
    <div class="data__stage">
      <div class="data__stream data__stream--top" aria-hidden="true">
        <span v-for="(field, index) in [...fields, ...fields]" :key="`top-${field}-${index}`">
          {{ field }}
        </span>
      </div>

      <header class="data__header page-width">
        <p>Datos que abren caminos</p>
        <span>Información útil, abierta y reutilizable</span>
      </header>

      <div class="data__radar" aria-hidden="true">
        <span class="data__radar-ring data__radar-ring--edge"></span>
        <span class="data__radar-ring data__radar-ring--middle"></span>
        <span class="data__radar-ring data__radar-ring--core"></span>
        <span class="data__radar-ring data__radar-ring--broken"></span>
        <span class="data__radar-axis data__radar-axis--horizontal"></span>
        <span class="data__radar-axis data__radar-axis--vertical"></span>
        <span class="data__radar-sweep"></span>
        <i class="data__radar-signal data__radar-signal--one"></i>
        <i class="data__radar-signal data__radar-signal--two"></i>
        <i class="data__radar-signal data__radar-signal--three"></i>
      </div>

      <h2 id="data-title" class="data__title" aria-label="Cultura abierta">
        <span class="data__title-row" aria-hidden="true">
          <i class="data__title-outline" data-text="Cultura">Cultura</i>
        </span>
        <span class="data__title-row" aria-hidden="true">
          <i class="data__title-outline" data-text="Abierta">Abierta</i>
        </span>
      </h2>

      <ul class="data__uses" aria-label="Usos de los datos abiertos">
        <li v-for="use in uses" :key="use" class="data__use"><i></i>{{ use }}</li>
      </ul>

      <div class="data__stream data__stream--bottom" aria-hidden="true">
        <span v-for="(use, index) in [...uses, ...uses, ...uses]" :key="`bottom-${use}-${index}`">
          {{ use }}
        </span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.data {
  --radar-mint: #19b39a;
  --radar-gold: #d8a94e;
  position: relative;
  z-index: 3;
  overflow: clip;
  color: #f7f8fa;
  background: #08090d;
}
.data__stage {
  position: relative;
  display: grid;
  place-items: center;
  min-height: 100svh;
  overflow: hidden;
  padding-block: calc(var(--header) + 2rem) 4rem;
}
.data__header {
  position: absolute;
  z-index: 7;
  top: calc(var(--header) + 2rem);
  right: 0;
  left: 0;
  display: flex;
  justify-content: space-between;
  color: #aeb2bd;
  font-size: 0.68rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.data__header p,
.data__header span {
  margin: 0;
}
.data__header p {
  color: #f7f8fa;
}
.data__title {
  --title-reveal: 0%;
  position: relative;
  z-index: 4;
  display: grid;
  justify-items: center;
  margin: 0;
  color: transparent;
  font-family: var(--display);
  font-size: clamp(6rem, 13vw, 13.5rem);
  font-weight: 650;
  line-height: 0.72;
  letter-spacing: -0.075em;
  text-transform: uppercase;
}
.data__title-row,
.data__title-row i {
  position: relative;
  display: block;
}
.data__title-row i {
  font-style: normal;
  white-space: nowrap;
}
.data__title-outline {
  color: transparent;
  -webkit-text-stroke: 1px rgb(247 248 250 / 0.66);
}
.data__title-outline::after {
  position: absolute;
  inset: 0;
  color: #f7f8fa;
  clip-path: inset(0 calc(100% - var(--title-reveal)) 0 0);
  content: attr(data-text);
  -webkit-text-stroke: 0;
  will-change: clip-path;
}
.data__radar {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 50%;
  width: min(26vw, 23rem);
  min-width: 17rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgb(109 74 255 / 0.1), transparent 66%);
  transform: translate(-50%, -50%);
  will-change: transform, opacity;
}
.data__radar-ring,
.data__radar-axis,
.data__radar-sweep,
.data__radar-signal {
  position: absolute;
  display: block;
}
.data__radar-ring {
  border: 1px solid rgb(247 248 250 / 0.24);
  border-radius: 50%;
}
.data__radar-ring--edge {
  inset: 2%;
}
.data__radar-ring--middle {
  inset: 22%;
}
.data__radar-ring--core {
  inset: 42%;
  border-color: color-mix(in srgb, var(--radar-mint) 55%, transparent);
}
.data__radar-ring--broken {
  inset: 11%;
  border-color: rgb(255 91 91 / 0.68) transparent rgb(109 74 255 / 0.5);
  will-change: transform;
}
.data__radar-axis {
  top: 50%;
  left: 8%;
  width: 84%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgb(247 248 250 / 0.2), transparent);
}
.data__radar-axis--vertical {
  transform: rotate(90deg);
}
.data__radar-sweep {
  top: 50%;
  left: 50%;
  width: 46%;
  height: 46%;
  background: conic-gradient(
    from 250deg at 0 0,
    transparent 0deg,
    rgb(25 179 154 / 0.35) 32deg,
    transparent 34deg
  );
  transform-origin: 0 0;
  will-change: transform;
}
.data__radar-signal {
  width: 0.46rem;
  height: 0.46rem;
  border-radius: 50%;
  background: #f7f8fa;
  box-shadow:
    0 0 0 0.42rem rgb(247 248 250 / 0.08),
    0 0 1.4rem rgb(25 179 154 / 0.76);
  will-change: transform, opacity;
}
.data__radar-signal--one {
  top: 25%;
  left: 61%;
}
.data__radar-signal--two {
  top: 61%;
  left: 23%;
  background: var(--coral);
}
.data__radar-signal--three {
  right: 19%;
  bottom: 21%;
  background: var(--radar-gold);
}
.data__uses {
  position: absolute;
  z-index: 7;
  right: 0;
  bottom: 2.1rem;
  left: 0;
  display: flex;
  justify-content: center;
  gap: clamp(1.5rem, 5vw, 5rem);
  margin: 0;
  padding: 0;
  list-style: none;
}
.data__use {
  display: flex;
  gap: 0.55rem;
  align-items: center;
  color: #c3c6cf;
  font-size: 0.66rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  will-change: transform, opacity;
}
.data__use i {
  width: 0.52rem;
  height: 0.52rem;
  border-radius: 50%;
  background: var(--coral);
}
.data__use:nth-child(2) i {
  background: var(--blue);
}
.data__use:nth-child(3) i {
  background: var(--radar-gold);
}
.data__stream {
  position: absolute;
  z-index: 1;
  display: flex;
  gap: clamp(3rem, 8vw, 9rem);
  width: 120%;
  color: rgb(247 248 250 / 0.12);
  font-family: var(--display);
  font-size: clamp(1rem, 1.6vw, 1.75rem);
  font-weight: 650;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
  will-change: transform;
}
.data__stream--top {
  top: 18%;
  left: -2%;
}
.data__stream--bottom {
  right: -2%;
  bottom: 15%;
  justify-content: flex-end;
}

@media (max-width: 820px) {
  .data__stage {
    min-height: 54rem;
    padding-block: calc(var(--header) + 5rem) 6rem;
  }
  .data__header {
    top: calc(var(--header) + 2rem);
    display: grid;
    gap: 0.35rem;
  }
  .data__title {
    --title-reveal: 100%;
    font-size: clamp(4.4rem, 18vw, 8rem);
    line-height: 0.78;
  }
  .data__radar {
    width: min(54vw, 20rem);
    min-width: 15rem;
  }
  .data__uses {
    bottom: 5rem;
    flex-wrap: wrap;
  }
  .data__stream--top {
    display: none;
  }
}

@media (max-width: 430px) {
  .data__stage {
    min-height: 48rem;
  }
  .data__header span {
    display: none;
  }
  .data__title {
    font-size: clamp(3.5rem, 17vw, 4.3rem);
  }
  .data__radar {
    width: 58vw;
    min-width: 13.5rem;
  }
  .data__uses {
    gap: 1.15rem;
  }
  .data__stream {
    font-size: 0.9rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .data__radar,
  .data__radar-ring,
  .data__radar-sweep,
  .data__radar-signal,
  .data__use,
  .data__stream {
    opacity: 1;
  }
  .data__title {
    --title-reveal: 100%;
  }
}
</style>
