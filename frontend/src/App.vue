<script setup lang="ts">
import BrandMark from './components/BrandMark.vue'
import FeatureBand from './components/FeatureBand.vue'
import RadarField from './components/RadarField.vue'
</script>

<template>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <div class="site-shell">
    <header class="site-header">
      <BrandMark />
    </header>

    <main id="contenido">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero__copy">
          <h1 id="hero-title">Próximamente</h1>
          <p class="hero__name">Radar Cultural</p>
          <p class="hero__mission">
            Conectamos a las personas con eventos, experiencias y espacios culturales.
          </p>
        </div>
        <RadarField class="hero__visual" />
      </section>

      <FeatureBand />
    </main>

    <footer class="site-footer">
      <p>La plataforma se encuentra en desarrollo.</p>
      <div class="site-footer__signature">
        <span>Radar Cultural</span>
        <span>México</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.site-shell {
  width: min(calc(100% - 2rem), 96rem);
  margin-inline: auto;
}

.site-header {
  display: flex;
  align-items: center;
  min-height: 6.5rem;
  border-bottom: 1px solid var(--color-line);
}

.hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 0.88fr) minmax(30rem, 1.12fr);
  align-items: center;
  min-height: min(46rem, calc(100svh - 6.5rem));
  overflow: hidden;
}

.hero::before,
.hero::after {
  position: absolute;
  z-index: -1;
  content: '';
}

.hero::before {
  inset: 8% 0 8% 46%;
  background-image:
    linear-gradient(var(--color-line-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-line-soft) 1px, transparent 1px);
  background-size: 9.5rem 9.5rem;
  mask-image: radial-gradient(circle at 55% 50%, #000, transparent 72%);
}

.hero::after {
  bottom: 8%;
  left: -12%;
  width: 38rem;
  height: 15rem;
  border-radius: 50%;
  background: repeating-radial-gradient(
    ellipse at 50% 100%,
    transparent 0 0.75rem,
    rgb(39 212 202 / 0.12) 0.8rem 0.86rem
  );
  transform: rotate(8deg);
  mask-image: linear-gradient(to right, #000, transparent 80%);
}

.hero__copy {
  position: relative;
  z-index: 2;
  min-width: 0;
  padding: clamp(5rem, 11vh, 8rem) 0;
}

.hero h1 {
  max-width: 10ch;
  margin: 0;
  color: var(--color-text);
  font-size: clamp(4.25rem, 8.5vw, 9rem);
  font-weight: 580;
  line-height: 0.88;
  letter-spacing: -0.075em;
}

.hero__name {
  margin: 1.5rem 0 0;
  color: var(--color-text);
  font-size: clamp(2rem, 4.2vw, 4.5rem);
  font-weight: 380;
  line-height: 1;
  letter-spacing: -0.045em;
}

.hero__mission {
  max-width: 34rem;
  margin: 2rem 0 0;
  color: var(--color-muted);
  font-size: clamp(1.1rem, 1.55vw, 1.45rem);
  line-height: 1.55;
}

.hero__visual {
  justify-self: end;
  margin-right: -7%;
}

.site-footer {
  display: flex;
  justify-content: space-between;
  gap: 3rem;
  padding: clamp(3rem, 6vw, 5.5rem) clamp(0rem, 2vw, 2rem);
  color: var(--color-muted);
}

.site-footer p {
  margin: 0;
  font-size: clamp(1rem, 1.4vw, 1.2rem);
}

.site-footer__signature {
  display: grid;
  min-width: 11rem;
  padding-left: 2rem;
  border-left: 1px solid var(--color-line);
  color: var(--color-text);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  line-height: 1.7;
  letter-spacing: 0.08em;
}

@media (max-width: 1040px) {
  .hero {
    grid-template-columns: minmax(0, 0.9fr) minmax(26rem, 1.1fr);
  }

  .hero__visual {
    margin-right: -17%;
  }
}

@media (max-width: 760px) {
  .site-shell {
    width: min(calc(100% - 1.25rem), 96rem);
  }

  .site-header {
    min-height: 5rem;
  }

  .hero {
    grid-template-columns: minmax(0, 1fr);
    min-height: auto;
    padding-top: 2rem;
  }

  .hero::before {
    inset: 42% -30% 2% 0;
  }

  .hero::after {
    display: none;
  }

  .hero__copy {
    padding: 3rem 0 0;
  }

  .hero h1 {
    font-size: clamp(3.1rem, 16.2vw, 5.6rem);
  }

  .hero__name {
    font-size: clamp(2rem, 10vw, 3.5rem);
  }

  .hero__mission {
    max-width: 28rem;
    margin-top: 1.5rem;
    font-size: 1.05rem;
  }

  .hero__visual {
    justify-self: center;
    margin-top: -1rem;
    margin-right: 0;
  }

  .site-footer {
    flex-direction: column;
    padding-inline: 1.5rem;
  }

  .site-footer__signature {
    padding-top: 1rem;
    padding-left: 0;
    border-top: 1px solid var(--color-line);
    border-left: 0;
  }
}
</style>
