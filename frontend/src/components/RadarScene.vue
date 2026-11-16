<script setup lang="ts">
import { computed } from 'vue'
import type { CulturalEvent } from '../api/radar'
import { formatEventTeaserDate } from '../api/formatDate'
import architecture from '../assets/hero-day.webp'
import workshop from '../assets/community-workshop.webp'
import dance from '../assets/fragment-dance.webp'
import cinema from '../assets/fragment-cinema.webp'

const props = defineProps<{ events: CulturalEvent[] }>()

function briefCredit(credit: string): string {
  if (credit.includes('Radar Cultural')) return 'Radar Cultural'
  if (credit.length <= 18) return credit
  const words = credit.slice(0, 19).trimEnd().split(' ')
  if (words.length > 1) words.pop()
  return `${words.join(' ')}…`
}

const editorialFragments = [
  {
    src: dance,
    className: 'fragment--dance',
    width: 1280,
    height: 960,
    drift: '18px',
    tilt: '-5deg',
  },
  {
    src: workshop,
    className: 'fragment--workshop',
    width: 1122,
    height: 1402,
    drift: '-14px',
    tilt: '4deg',
  },
  {
    src: architecture,
    className: 'fragment--architecture',
    width: 1585,
    height: 992,
    drift: '15px',
    tilt: '3deg',
  },
  {
    src: cinema,
    className: 'fragment--music',
    width: 1120,
    height: 1120,
    drift: '-12px',
    tilt: '0deg',
  },
] as const

const fragments = computed(() =>
  editorialFragments.map((fragment, index) => ({
    ...fragment,
    event: props.events[index] ?? null,
    src: props.events[index]?.image?.url ?? fragment.src,
  })),
)
</script>

<template>
  <div class="culture-fragments">
    <figure
      v-for="(fragment, index) in fragments"
      :key="fragment.className"
      class="fragment-slot"
      :class="[fragment.className, { 'fragment-slot--linked': fragment.event }]"
    >
      <div class="fragment-frame">
        <div class="fragment-card" :style="{ '--drift': fragment.drift, '--tilt': fragment.tilt }">
          <a
            v-if="fragment.event"
            class="fragment-media fragment-media--event"
            :href="`/eventos/${encodeURIComponent(fragment.event.slug)}/`"
          >
            <img
              :src="fragment.src"
              alt=""
              :width="fragment.width"
              :height="fragment.height"
              :loading="index < 2 ? 'eager' : 'lazy'"
              decoding="async"
            />
            <small
              v-if="fragment.event.image"
              class="fragment-credit"
              :title="`Crédito de imagen: ${fragment.event.image.credit}`"
              >Foto: {{ briefCredit(fragment.event.image.credit) }}</small
            >
            <span class="fragment-caption">
              <time :datetime="fragment.event.starts_at">
                {{ formatEventTeaserDate(fragment.event.starts_at, fragment.event.time_zone) }}
              </time>
              <strong :lang="fragment.event.language_code || undefined">{{
                fragment.event.title
              }}</strong>
            </span>
          </a>
          <div v-else class="fragment-media" aria-hidden="true">
            <img
              :src="fragment.src"
              alt=""
              :width="fragment.width"
              :height="fragment.height"
              :fetchpriority="index < 2 ? 'high' : 'auto'"
            />
          </div>
        </div>
      </div>
    </figure>
  </div>
</template>

<style scoped>
.culture-fragments {
  position: absolute;
  z-index: 1;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}
.fragment-slot {
  position: absolute;
  margin: 0;
  will-change: transform, filter, opacity;
}
.fragment-slot--linked {
  pointer-events: auto;
}
.fragment-frame {
  width: 100%;
  height: 100%;
}
.fragment-card {
  width: 100%;
  height: 100%;
  padding: clamp(0.25rem, 0.42vw, 0.42rem);
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--text) 24%, transparent);
  background: color-mix(in srgb, var(--acrylic-strong) 88%, transparent);
  box-shadow: 0 1.25rem 4rem rgb(8 9 13 / 0.18);
  animation: cultural-drift 5.8s ease-in-out infinite alternate;
  backdrop-filter: blur(18px) saturate(145%);
  -webkit-backdrop-filter: blur(18px) saturate(145%);
  will-change: transform;
}
.fragment-media {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: inherit;
}
.fragment-media--event {
  color: #fff;
  text-decoration: none;
  animation: fragment-reveal 650ms var(--ease-out) both;
}
@keyframes fragment-reveal {
  from {
    opacity: 0;
    transform: translateY(-1.25rem) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
.fragment-caption {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 2.5rem 0.75rem 0.7rem;
  background: linear-gradient(transparent, rgb(8 9 13 / 0.8));
  font-size: clamp(0.78rem, 0.95vw, 0.9rem);
  font-weight: 700;
  line-height: 1.2;
  text-wrap: balance;
}
.fragment-caption strong,
.fragment-caption time,
.fragment-caption small {
  display: block;
}
.fragment-caption time {
  margin-bottom: 0.3rem;
  overflow: hidden;
  font-size: 0.72rem;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.fragment-caption strong {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
.fragment-credit {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 1;
  max-width: calc(100% - 1rem);
  padding: 0.23rem 0.4rem;
  overflow: hidden;
  border: 1px solid rgb(255 255 255 / 0.22);
  border-radius: 0.25rem;
  color: #fff;
  background: rgb(8 9 13 / 0.52);
  font-size: 0.63rem;
  font-weight: 500;
  line-height: 1.2;
  text-overflow: ellipsis;
  white-space: nowrap;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.fragment--music .fragment-caption {
  right: 10%;
  bottom: 10%;
  left: 10%;
  padding: 1.5rem 0.2rem 0.25rem;
  font-size: clamp(0.6rem, 0.8vw, 0.74rem);
  text-align: center;
}
.fragment-media--event:focus-visible {
  outline: 3px solid var(--coral);
  outline-offset: -3px;
}
.fragment-slot:nth-child(2n) .fragment-card {
  animation-duration: 7.1s;
  animation-delay: -2.4s;
}
.fragment-slot:nth-child(3n) .fragment-card {
  animation-duration: 6.4s;
  animation-delay: -4.1s;
}
.fragment-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.fragment--dance {
  top: 12%;
  left: 4.5%;
  width: clamp(12rem, 21vw, 24rem);
  aspect-ratio: 4 / 3;
}
.fragment--workshop {
  top: 9%;
  right: 7%;
  width: clamp(9.5rem, 15vw, 16.5rem);
  aspect-ratio: 4 / 5;
}
.fragment--music .fragment-card {
  border-radius: 50%;
}
.fragment--music.fragment-slot--linked {
  width: clamp(11rem, 17vw, 18rem);
  aspect-ratio: 4 / 3;
}
.fragment--music.fragment-slot--linked .fragment-card {
  border-radius: 0;
}
.fragment--music.fragment-slot--linked .fragment-caption {
  right: 0;
  bottom: 0;
  left: 0;
  padding: 2.5rem 0.75rem 0.7rem;
  font-size: clamp(0.78rem, 0.95vw, 0.9rem);
  text-align: left;
}
.fragment--architecture {
  bottom: 3.5%;
  left: 8%;
  width: clamp(12rem, 22vw, 25rem);
  aspect-ratio: 16 / 10;
}
.fragment--music {
  right: 9%;
  bottom: 2.5%;
  width: clamp(9rem, 14vw, 15rem);
  aspect-ratio: 1;
}
@keyframes cultural-drift {
  from {
    transform: translate3d(0, calc(var(--drift) * -0.5), 0) rotate(calc(var(--tilt) - 0.75deg));
  }
  to {
    transform: translate3d(0, var(--drift), 0) rotate(calc(var(--tilt) + 0.75deg));
  }
}
@media (max-width: 800px) {
  .fragment-slot:nth-child(n + 3) {
    display: none;
  }
  .fragment-caption {
    padding: 1.8rem 0.55rem 0.5rem;
    font-size: 0.84rem;
  }
  .fragment--dance {
    top: 14%;
    left: 0;
    width: 46vw;
  }
  .fragment--workshop {
    top: 11%;
    right: 0;
    width: 42vw;
  }
  .fragment--architecture {
    bottom: -5%;
    left: 8%;
    width: 49vw;
  }
  .fragment--music {
    right: 2%;
    bottom: -2%;
    width: 31vw;
  }
}
@media (min-width: 601px) and (max-width: 800px) {
  .fragment--dance {
    top: 11%;
    width: 36vw;
  }
  .fragment--workshop {
    top: 9%;
    width: 26vw;
  }
}
@media (prefers-reduced-motion: reduce) {
  .fragment-card,
  .fragment-media--event {
    animation: none;
  }
}
</style>
