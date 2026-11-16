<script setup lang="ts">
import { onMounted } from 'vue'
import CommunitySection from './components/CommunitySection.vue'
import AgendaPage from './components/AgendaPage.vue'
import DataSection from './components/DataSection.vue'
import EventPage from './components/EventPage.vue'
import HeroSection from './components/HeroSection.vue'
import InformationPage from './components/InformationPage.vue'
import IntroSequence from './components/IntroSequence.vue'
import SiteFooter from './components/SiteFooter.vue'
import SiteHeader from './components/SiteHeader.vue'
import VisionSection from './components/VisionSection.vue'
import { initTheme } from './composables/useTheme'

const path = window.location.pathname
const isHome = path === '/'
const isAgenda = path === '/agenda/'
const eventSlug = path.match(/^\/eventos\/([^/]+)\/$/)?.[1]
const informationPage =
  path === '/privacidad/'
    ? 'privacy'
    : path === '/terminos/'
      ? 'terms'
      : path === '/codigo-de-conducta/'
        ? 'conduct'
        : null

onMounted(initTheme)
</script>

<template>
  <IntroSequence v-if="isHome" />
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <SiteHeader :home="isHome" />
  <main id="contenido">
    <template v-if="isHome">
      <HeroSection />
      <VisionSection />
      <DataSection />
      <CommunitySection />
    </template>
    <AgendaPage v-else-if="isAgenda" />
    <EventPage v-else-if="eventSlug" :slug="eventSlug" />
    <InformationPage v-else-if="informationPage" :page="informationPage" />
    <AgendaPage v-else />
  </main>
  <SiteFooter />
</template>
