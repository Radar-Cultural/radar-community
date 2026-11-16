import { createApp } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import App from './App.vue'
import { reveal } from './directives/reveal'
import './styles/base.css'

gsap.registerPlugin(ScrollTrigger)

createApp(App).directive('reveal', reveal).mount('#app')

window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true })
void document.fonts.ready.then(() => ScrollTrigger.refresh())
