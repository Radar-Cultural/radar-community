<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { listEvents, type CulturalEvent, type PaginatedResponse } from '../api/radar'
import { setPageMeta } from '../api/pageMeta'
import { formatEventDate } from '../api/formatDate'

const events = ref<CulturalEvent[]>([])
const state = ref<'loading' | 'ready' | 'error'>('loading')
const search = ref('')
const submittedSearch = ref('')
const page = ref(1)
const total = ref(0)
const hasNext = ref(false)
const agendaInstant = new Date().toISOString()
let request: AbortController | undefined

async function load() {
  request?.abort()
  request = new AbortController()
  state.value = 'loading'
  try {
    const data: PaginatedResponse<CulturalEvent> = await listEvents(
      {
        q: submittedSearch.value,
        not_finished_at: agendaInstant,
        status: 'EventScheduled',
        ordering: 'starts_at',
        page: page.value,
        page_size: 12,
      },
      request.signal,
    )
    events.value = data.results
    total.value = data.count
    hasNext.value = Boolean(data.next)
    state.value = 'ready'
  } catch (error) {
    if (!(error instanceof DOMException && error.name === 'AbortError')) state.value = 'error'
  }
}

function submitSearch() {
  submittedSearch.value = search.value.trim().slice(0, 120)
  page.value = 1
  void load()
}

function changePage(nextPage: number) {
  page.value = nextPage
  void load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  setPageMeta(
    'Agenda cultural',
    'Explora eventos culturales publicados con fuente verificable en Radar Cultural.',
  )
  void load()
})
onUnmounted(() => request?.abort())
</script>

<template>
  <section class="agenda page-width" aria-labelledby="agenda-title">
    <header class="agenda__intro">
      <p class="agenda__eyebrow">La cultura sucede</p>
      <h1 id="agenda-title">Agenda cultural</h1>
      <p>
        Eventos publicados con fuente verificable. Explora lo que viene y encuentra un lugar para
        estar.
      </p>
    </header>

    <form class="agenda__search" role="search" @submit.prevent="submitSearch">
      <label for="agenda-query">Buscar eventos</label>
      <div>
        <input
          id="agenda-query"
          v-model="search"
          type="search"
          maxlength="120"
          placeholder="Música, cine, talleres…"
        />
        <button type="submit" :disabled="state === 'loading'">
          {{ state === 'loading' ? 'Buscando…' : 'Buscar' }}
        </button>
      </div>
    </form>

    <p v-if="state === 'loading'" class="agenda__message" role="status">Cargando la agenda…</p>
    <div v-else-if="state === 'error'" class="agenda__message" role="alert">
      <p>No se pudo consultar la agenda en este momento.</p>
      <button type="button" @click="load">Volver a intentar</button>
    </div>
    <div v-else-if="events.length === 0" class="agenda__message" role="status">
      <h2>
        {{
          submittedSearch ? 'No encontramos coincidencias' : 'La agenda todavía está por abrirse'
        }}
      </h2>
      <p>
        {{
          submittedSearch
            ? 'Prueba con otra búsqueda.'
            : 'Publicaremos eventos cuando sus fuentes y datos estén verificados.'
        }}
      </p>
    </div>
    <template v-else>
      <p class="agenda__count" role="status">
        {{ total }} {{ total === 1 ? 'evento' : 'eventos' }}
      </p>
      <div class="agenda__grid">
        <article v-for="event in events" :key="event.id" class="agenda__card">
          <a :href="`/eventos/${encodeURIComponent(event.slug)}/`">
            <img
              v-if="event.image"
              :src="event.image.url"
              :alt="`Imagen de ${event.title}. Crédito: ${event.image.credit}`"
              loading="lazy"
            />
            <div v-else class="agenda__image-fallback" aria-hidden="true">
              <span>Radar<br />Cultural</span>
            </div>
            <div class="agenda__card-copy">
              <p>{{ formatEventDate(event.starts_at, event.time_zone, 'long') }}</p>
              <h2 :lang="event.language_code || undefined">{{ event.title }}</h2>
              <span>{{
                event.place?.name || (event.online_url ? 'En línea' : 'Lugar por confirmar')
              }}</span>
            </div>
          </a>
        </article>
      </div>
      <nav class="agenda__pages" aria-label="Páginas de la agenda">
        <button type="button" :disabled="page === 1" @click="changePage(page - 1)">Anterior</button>
        <span>Página {{ page }}</span>
        <button type="button" :disabled="!hasNext" @click="changePage(page + 1)">Siguiente</button>
      </nav>
    </template>
  </section>
</template>

<style scoped>
.agenda {
  min-height: 75vh;
  padding-block: calc(var(--header) + 5rem) 7rem;
}
.agenda__intro {
  max-width: 55rem;
}
.agenda__eyebrow {
  color: var(--wine);
  font-weight: 750;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.agenda h1 {
  margin: 0.5rem 0 1.3rem;
  font-family: var(--display);
  font-size: clamp(3.6rem, 8vw, 7.5rem);
  line-height: 0.95;
  letter-spacing: -0.065em;
}
.agenda__intro > p:last-child {
  max-width: 36rem;
  color: var(--text-soft);
  font-size: 1.12rem;
  line-height: 1.6;
}
.agenda__search {
  display: grid;
  gap: 0.5rem;
  max-width: 42rem;
  margin-block: 3rem;
  font-weight: 700;
}
.agenda__search > div {
  display: flex;
  gap: 0.7rem;
}
.agenda__search input {
  flex: 1;
  min-width: 0;
  padding: 0.9rem 1rem;
  border: 1px solid var(--line-strong);
  border-radius: 0.35rem;
  color: var(--text);
  background: var(--surface);
  font: inherit;
}
.agenda button {
  padding: 0.85rem 1.2rem;
  border: 1px solid var(--line-strong);
  border-radius: 0.35rem;
  color: var(--text);
  background: var(--surface);
  font: inherit;
  font-weight: 700;
}
.agenda__search button {
  color: #fff;
  background: var(--blue);
}
.agenda button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
.agenda__message {
  max-width: 42rem;
  min-height: 12rem;
  padding: 2rem;
  border: 1px solid var(--line);
  border-radius: 0.8rem;
  background: var(--surface);
  line-height: 1.6;
}
.agenda__message h2 {
  font-family: var(--display);
  font-size: 1.5rem;
}
.agenda__count {
  color: var(--text-soft);
}
.agenda__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}
.agenda__card {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 0.8rem;
  background: var(--surface);
}
.agenda__card a {
  display: block;
  height: 100%;
  color: inherit;
  text-decoration: none;
}
.agenda__card img,
.agenda__image-fallback {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
.agenda__image-fallback {
  display: grid;
  place-items: center;
  color: #fff;
  background: linear-gradient(135deg, var(--wine), var(--blue));
  font-family: var(--display);
  font-size: 2rem;
  line-height: 0.9;
}
.agenda__card-copy {
  padding: 1.25rem;
}
.agenda__card-copy p {
  margin: 0;
  color: var(--text-soft);
  font-size: 0.83rem;
}
.agenda__card-copy h2 {
  margin: 0.8rem 0;
  font-family: var(--display);
  font-size: 1.6rem;
  line-height: 1.1;
}
.agenda__card-copy span {
  color: var(--text-soft);
  font-size: 0.9rem;
}
.agenda__pages {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  margin-top: 2rem;
}
@media (max-width: 900px) {
  .agenda__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 600px) {
  .agenda {
    padding-top: calc(var(--header) + 3rem);
  }
  .agenda__grid {
    grid-template-columns: 1fr;
  }
  .agenda__search > div {
    flex-wrap: wrap;
  }
  .agenda__search button {
    width: 100%;
  }
}
</style>
