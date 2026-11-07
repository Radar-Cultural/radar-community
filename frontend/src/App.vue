<script setup lang="ts">
import { onMounted } from 'vue'
import CommunitySection from './components/CommunitySection.vue'
import DataSection from './components/DataSection.vue'
import HeroSection from './components/HeroSection.vue'
import IntroSequence from './components/IntroSequence.vue'
import SiteFooter from './components/SiteFooter.vue'
import SiteHeader from './components/SiteHeader.vue'
import VisionSection from './components/VisionSection.vue'
import { initTheme } from './composables/useTheme'

onMounted(initTheme)
</script>

<template>
  <IntroSequence />
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <SiteHeader />
  <main id="contenido">
    <HeroSection />
    <VisionSection />
    <DataSection />
    <CommunitySection />
  </main>
  <SiteFooter />
</template>
