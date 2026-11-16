<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'

const phases = [
  {
    verb: 'Detectar',
    label: 'Lo que sucede',
    copy: 'Eventos, experiencias y espacios entran en el radar.',
  },
  {
    verb: 'Orientar',
    label: 'Lo que necesitas',
    copy: 'Qué ocurre, dónde, cuándo y cómo participar.',
  },
  {
    verb: 'Amplificar',
    label: 'Lo que se comparte',
    copy: 'La información circula para conectar cultura y personas.',
  },
] as const

const disciplines = ['Música', 'Cine', 'Danza', 'Museos', 'Teatro', 'Literatura'] as const

const root = ref<HTMLElement | null>(null)
const active = ref(0)
let context: gsap.Context | undefined
let media: gsap.MatchMedia | undefined

onMounted(() => {
  if (!root.value || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  context = gsap.context(() => {
    media = gsap.matchMedia()

    media.add('(min-width: 821px)', () => {
      const board = root.value?.querySelector<HTMLElement>('.vision__board')
      const scanner = root.value?.querySelector<HTMLElement>('.vision__scanner')
      if (!board || !scanner) return

      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: '.vision__stage',
          start: 'top top',
          end: '+=1900',
          pin: true,
          scrub: 0.7,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onUpdate: (self) => {
            active.value = Math.min(phases.length - 1, Math.floor(self.progress * phases.length))
          },
        },
      })

      timeline
        .fromTo(
          scanner,
          { x: 0 },
          {
            x: () => Math.max(0, board.clientWidth - scanner.offsetWidth - 4),
            duration: 1,
            ease: 'none',
          },
          0,
        )
        .fromTo(
          '.vision__discipline',
          { opacity: 0.16, y: 18 },
          { opacity: 1, y: 0, duration: 0.16, stagger: 0.125, ease: 'power2.out' },
          0.05,
        )
        .fromTo(
          '.vision__wave-live',
          { clipPath: 'inset(0 100% 0 0)' },
          { clipPath: 'inset(0 0% 0 0)', duration: 1, ease: 'none' },
          0,
        )
        .fromTo(
          '.vision__phase-line',
          { scaleX: 0 },
          { scaleX: 1, duration: 0.2, stagger: 0.28, ease: 'power2.out' },
          0.08,
        )
    })

    media.add('(max-width: 820px)', () => {
      const board = root.value?.querySelector<HTMLElement>('.vision__board')
      const scanner = root.value?.querySelector<HTMLElement>('.vision__scanner')
      if (!board || !scanner) return

      gsap.fromTo(
        scanner,
        { x: 0 },
        {
          x: () => Math.max(0, board.clientWidth - scanner.offsetWidth - 4),
          ease: 'none',
          scrollTrigger: {
            trigger: board,
            start: 'top 76%',
            end: 'bottom 24%',
            scrub: 0.7,
            invalidateOnRefresh: true,
          },
        },
      )

      gsap.from('.vision__discipline', {
        y: 24,
        stagger: 0.07,
        duration: 0.75,
        ease: 'power3.out',
        scrollTrigger: { trigger: board, start: 'top 72%' },
      })

      gsap.from('.vision__phase', {
        y: 16,
        stagger: 0.08,
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: { trigger: board, start: 'top 72%' },
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
  <section id="proyecto" ref="root" class="vision" aria-labelledby="vision-title">
    <div class="vision__stage page-width">
      <header class="vision__heading">
        <p>Cómo circula la cultura</p>
        <h2 id="vision-title" class="vision__title display-title">
          Detectamos lo que sucede para que la cultura llegue más lejos.
        </h2>
      </header>

      <div class="vision__board" aria-label="Espectro de difusión cultural">
        <div class="vision__board-head">
          <span>Actividad cultural</span>
          <span>Difusión en movimiento</span>
        </div>

        <div class="vision__spectrum" aria-hidden="true">
          <div class="vision__disciplines">
            <span v-for="discipline in disciplines" :key="discipline" class="vision__discipline">
              {{ discipline }}
            </span>
          </div>

          <svg class="vision__wave" viewBox="0 0 1200 220" preserveAspectRatio="none">
            <path
              class="vision__wave-base"
              pathLength="1"
              d="M0 116C74 116 72 58 140 58S204 168 278 168s70-122 144-122 72 89 143 89 71-47 143-47 75 111 149 111 74-146 149-146 80 82 194 82"
            />
            <path
              class="vision__wave-live"
              pathLength="1"
              d="M0 116C74 116 72 58 140 58S204 168 278 168s70-122 144-122 72 89 143 89 71-47 143-47 75 111 149 111 74-146 149-146 80 82 194 82"
            />
          </svg>

          <div class="vision__scanner"><i></i><span>Abierta</span></div>
        </div>

        <ol class="vision__phases">
          <li
            v-for="(phase, index) in phases"
            :key="phase.verb"
            class="vision__phase"
            :class="{ 'is-active': active === index }"
            :aria-current="active === index ? 'step' : undefined"
          >
            <span class="vision__phase-line" aria-hidden="true"></span>
            <em>{{ phase.label }}</em>
            <strong>{{ phase.verb }}</strong>
            <p>{{ phase.copy }}</p>
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>

<style scoped>
.vision {
  position: relative;
  z-index: 4;
  overflow: clip;
  color: var(--text);
  background: var(--canvas);
  transition:
    color 500ms var(--ease-out),
    background-color 500ms var(--ease-out);
}
.vision__stage {
  display: grid;
  align-content: center;
  min-height: 100svh;
  padding-block: calc(var(--header) + 2rem) 4rem;
}
.vision__heading {
  display: grid;
  grid-template-columns: minmax(12rem, 0.28fr) minmax(0, 1fr);
  gap: clamp(2rem, 6vw, 7rem);
  align-items: start;
}
.vision__heading > p {
  margin: 0.65rem 0 0;
  color: var(--text-soft);
  font-size: 0.72rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.vision__title {
  max-width: 15ch;
  font-size: clamp(3.1rem, 5.15vw, 5.65rem);
  line-height: 0.91;
}
.vision__board {
  position: relative;
  margin-top: clamp(2.4rem, 5vh, 4.5rem);
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 1.25rem;
  background: color-mix(in srgb, var(--acrylic) 82%, transparent);
  box-shadow: var(--shadow);
  backdrop-filter: blur(28px) saturate(145%);
  -webkit-backdrop-filter: blur(28px) saturate(145%);
}
.vision__board-head {
  display: flex;
  justify-content: space-between;
  padding: 0.85rem 1.1rem;
  border-bottom: 1px solid var(--line);
  color: var(--text-soft);
  font-size: 0.65rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.vision__board-head span:last-child {
  color: var(--coral);
}
.vision__spectrum {
  position: relative;
  min-height: clamp(11rem, 23vh, 15rem);
  overflow: hidden;
  background-image: linear-gradient(var(--line) 1px, transparent 1px);
  background-size: 100% 25%;
}
.vision__disciplines {
  position: absolute;
  z-index: 2;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  align-items: center;
  padding-inline: clamp(1rem, 3vw, 3rem);
}
.vision__discipline {
  color: var(--text);
  font-family: var(--display);
  font-size: clamp(1.25rem, 2.25vw, 2.75rem);
  font-weight: 650;
  letter-spacing: -0.05em;
  text-align: center;
  will-change: transform, opacity;
}
.vision__wave {
  position: absolute;
  z-index: 1;
  inset: 0;
  width: 100%;
  height: 100%;
}
.vision__wave-base,
.vision__wave-live {
  fill: none;
  vector-effect: non-scaling-stroke;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.vision__wave-base {
  stroke: var(--line-strong);
  stroke-width: 1.3;
}
.vision__wave-live {
  stroke: var(--blue);
  stroke-width: 2.7;
  clip-path: inset(0 100% 0 0);
  filter: drop-shadow(0 0 0.45rem rgb(74 96 255 / 0.3));
  will-change: clip-path;
}
.vision__scanner {
  position: absolute;
  z-index: 4;
  top: 0;
  bottom: 0;
  left: 0;
  width: 2.6rem;
  border-left: 1px solid var(--coral);
  background: linear-gradient(90deg, rgb(255 91 91 / 0.16), transparent);
  will-change: transform;
}
.vision__scanner i {
  position: absolute;
  top: 50%;
  left: -0.28rem;
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  background: var(--coral);
  box-shadow: 0 0 0 0.42rem rgb(255 91 91 / 0.13);
}
.vision__scanner span {
  position: absolute;
  top: 0.75rem;
  left: 0.55rem;
  color: var(--coral);
  font-size: 0.58rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  white-space: nowrap;
}
.vision__phases {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin: 0;
  padding: 0;
  list-style: none;
}
.vision__phase {
  position: relative;
  min-height: 8.5rem;
  padding: 1.2rem 1.25rem 1.35rem;
  border-top: 1px solid var(--line);
  border-right: 1px solid var(--line);
  opacity: 0.4;
  transition:
    opacity 300ms ease,
    background-color 300ms ease;
}
.vision__phase:last-child {
  border-right: 0;
}
.vision__phase.is-active {
  opacity: 1;
  background: color-mix(in srgb, var(--blue) 7%, transparent);
}
.vision__phase-line {
  position: absolute;
  top: -1px;
  right: 0;
  left: 0;
  height: 2px;
  background: var(--blue);
  transform-origin: 0 50%;
}
.vision__phase em {
  display: block;
  color: var(--text-soft);
  font-size: 0.62rem;
  font-style: normal;
  font-weight: 750;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}
.vision__phase strong {
  display: block;
  margin-top: 0.42rem;
  color: var(--text);
  font-family: var(--display);
  font-size: clamp(1.45rem, 2.1vw, 2.25rem);
  line-height: 1;
  letter-spacing: -0.04em;
}
.vision__phase p {
  max-width: 24rem;
  margin: 0.45rem 0 0;
  color: var(--text-soft);
  font-size: 0.88rem;
  line-height: 1.4;
}

@media (max-width: 820px) {
  .vision__stage {
    min-height: auto;
    padding-block: calc(var(--header) + 4rem) 5rem;
  }
  .vision__heading {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .vision__heading > p {
    margin: 0;
  }
  .vision__title {
    max-width: 12ch;
    font-size: clamp(2.8rem, 10.5vw, 5rem);
  }
  .vision__board {
    margin-top: 2.6rem;
  }
  .vision__spectrum {
    min-height: 20rem;
  }
  .vision__disciplines {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    padding: 2.2rem 1.3rem;
  }
  .vision__discipline {
    font-size: clamp(1.65rem, 7vw, 2.5rem);
  }
  .vision__phases {
    grid-template-columns: 1fr;
  }
  .vision__phase {
    min-height: auto;
    border-right: 0;
    opacity: 1;
  }
  .vision__phase-line {
    transform: scaleX(1);
  }
}

@media (max-width: 430px) {
  .vision__title {
    max-width: 100%;
    font-size: clamp(2.55rem, 12vw, 3.2rem);
  }
  .vision__board-head span:last-child {
    display: none;
  }
  .vision__spectrum {
    min-height: 18rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .vision__discipline,
  .vision__phase {
    opacity: 1;
    transform: none;
  }
  .vision__scanner {
    right: 0;
    left: auto;
    transform: none;
  }
  .vision__wave-live {
    clip-path: inset(0 0 0 0);
  }
  .vision__phase-line {
    transform: scaleX(1);
  }
}
</style>
