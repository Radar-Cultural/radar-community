<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { getEvent, type CulturalEvent } from '../api/radar'
import { setPageMeta } from '../api/pageMeta'
import { formatEventDate } from '../api/formatDate'

const props = defineProps<{ slug: string }>()
const event = ref<CulturalEvent | null>(null)
const state = ref<'loading' | 'ready' | 'missing' | 'error'>('loading')
const request = new AbortController()

async function load() {
  state.value = 'loading'
  try {
    event.value = await getEvent(props.slug, request.signal)
    state.value = 'ready'
    setPageMeta(event.value.title, event.value.summary)
  } catch (error) {
    if (request.signal.aborted) return
    state.value =
      error instanceof Error && 'status' in error && error.status === 404 ? 'missing' : 'error'
    if (state.value === 'missing') {
      setPageMeta(
        'Evento no disponible',
        'Este evento no está disponible en Radar Cultural.',
        'noindex, follow',
      )
    }
  }
}

onMounted(() => void load())
onUnmounted(() => request.abort())
</script>

<template>
  <article class="event-page page-width">
    <a class="event-page__back" href="/agenda/">← Volver a la agenda</a>
    <p v-if="state === 'loading'" role="status">Cargando el evento…</p>
    <div v-else-if="state === 'error'" role="alert">
      <h1>No pudimos cargar el evento</h1>
      <button type="button" @click="load">Volver a intentar</button>
    </div>
    <div v-else-if="state === 'missing'">
      <h1>Este evento no está disponible</h1>
      <p>Puede haberse retirado o todavía no estar publicado.</p>
    </div>
    <template v-else-if="event">
      <p class="event-page__eyebrow">Evento cultural · {{ event.organizer.name }}</p>
      <h1 :lang="event.language_code || undefined">{{ event.title }}</h1>
      <p class="event-page__summary" :lang="event.language_code || undefined">
        {{ event.summary }}
      </p>
      <img
        v-if="event.image"
        class="event-page__image"
        :src="event.image.url"
        :alt="`Imagen de ${event.title}`"
      />
      <div class="event-page__layout">
        <div>
          <h2>Sobre el evento</h2>
          <p class="event-page__description" :lang="event.language_code || undefined">
            {{ event.description }}
          </p>
          <p v-if="event.image" class="event-page__credit">
            Imagen: {{ event.image.credit }} ·
            <a :href="event.image.source_url">Fuente de la imagen</a>
          </p>
          <a :href="event.source_url" target="_blank" rel="noopener noreferrer"
            >Consultar fuente del evento ↗</a
          >
        </div>
        <aside aria-label="Información práctica">
          <h2>Cuándo y dónde</h2>
          <dl>
            <dt>Inicio</dt>
            <dd>{{ formatEventDate(event.starts_at, event.time_zone, 'full') }}</dd>
            <dt v-if="event.ends_at">Fin</dt>
            <dd v-if="event.ends_at">
              {{ formatEventDate(event.ends_at, event.time_zone, 'full') }}
            </dd>
            <dt>Lugar</dt>
            <dd>{{ event.place?.name || (event.online_url ? 'En línea' : 'Por confirmar') }}</dd>
            <dt v-if="event.place">Dirección</dt>
            <dd v-if="event.place">
              {{
                [
                  event.place.address,
                  event.place.locality,
                  event.place.region,
                  event.place.country_code,
                ]
                  .filter(Boolean)
                  .join(', ')
              }}
            </dd>
            <dt>Acceso</dt>
            <dd>
              {{
                event.admission_type === 'free'
                  ? 'Gratuito'
                  : 'Consulta opciones de entrada en la fuente'
              }}
            </dd>
          </dl>
          <a :href="event.calendar_url">Añadir al calendario ↓</a>
        </aside>
      </div>
    </template>
  </article>
</template>

<style scoped>
.event-page {
  min-height: 70vh;
  padding-block: calc(var(--header) + 4rem) 7rem;
}
.event-page__back {
  display: inline-block;
  margin-bottom: 3rem;
  color: var(--text-soft);
  text-decoration: none;
}
.event-page__eyebrow {
  color: var(--wine);
  font-weight: 700;
}
.event-page h1 {
  max-width: 65rem;
  margin: 0.5rem 0 1rem;
  font-family: var(--display);
  font-size: clamp(3rem, 7vw, 6.5rem);
  line-height: 0.98;
  letter-spacing: -0.06em;
}
.event-page__summary {
  max-width: 48rem;
  color: var(--text-soft);
  font-size: clamp(1.15rem, 2vw, 1.5rem);
  line-height: 1.5;
}
.event-page__image {
  width: 100%;
  max-height: 42rem;
  margin-block: 2rem;
  border-radius: 0.8rem;
  object-fit: cover;
}
.event-page__layout {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(16rem, 0.7fr);
  gap: clamp(2rem, 7vw, 7rem);
  margin-top: 3rem;
}
.event-page h2 {
  font-family: var(--display);
}
.event-page__description {
  white-space: pre-line;
  line-height: 1.8;
}
.event-page__credit {
  color: var(--text-soft);
  font-size: 0.85rem;
}
.event-page aside {
  align-self: start;
  padding: 1.5rem;
  border: 1px solid var(--line);
  border-radius: 0.8rem;
  background: var(--surface);
}
.event-page dl {
  display: grid;
  gap: 0.5rem;
}
.event-page dt {
  margin-top: 0.8rem;
  color: var(--text-soft);
  font-size: 0.8rem;
}
.event-page dd {
  margin: 0;
  line-height: 1.4;
}
.event-page a {
  color: inherit;
}
.event-page button {
  padding: 0.8rem 1rem;
  border: 1px solid var(--line-strong);
  color: var(--text);
  background: var(--surface);
  font: inherit;
}
@media (max-width: 700px) {
  .event-page__layout {
    grid-template-columns: 1fr;
  }
}
</style>
