<script setup lang="ts">
import { onMounted } from 'vue'
import { setPageMeta } from '../api/pageMeta'

const props = defineProps<{ page: 'privacy' | 'terms' | 'conduct' }>()

const titles = {
  privacy: 'Aviso de privacidad',
  terms: 'Términos y condiciones',
  conduct: 'Código de conducta',
}

const metaTitles = {
  privacy: 'Aviso de privacidad en preparación',
  terms: 'Términos y condiciones en preparación',
  conduct: 'Código de conducta',
}

onMounted(() => {
  setPageMeta(
    metaTitles[props.page],
    props.page === 'conduct'
      ? 'Normas de convivencia y participación de Radar Cultural.'
      : `${titles[props.page]} en preparación para Radar Cultural.`,
    props.page === 'conduct' ? 'index, follow' : 'noindex, follow',
  )
})
</script>

<template>
  <article class="information page-width">
    <a href="/">← Volver al inicio</a>
    <p class="information__eyebrow">Radar Cultural · Comunidad</p>
    <h1>{{ titles[page] }}</h1>

    <template v-if="page === 'privacy'">
      <p class="information__lead">Documento en preparación.</p>
      <p>
        El aviso integral se publicará cuando estén definidos y verificados la identidad y el
        domicilio de la persona o entidad responsable, el canal para ejercer derechos sobre datos
        personales, las finalidades, los plazos de conservación y los terceros que intervienen en el
        tratamiento.
      </p>
      <p>
        Esta página todavía no constituye un aviso de privacidad completo ni se presenta para
        obtener consentimiento. La consulta pública de eventos no requiere crear una cuenta.
      </p>
    </template>

    <template v-else-if="page === 'terms'">
      <p class="information__lead">Documento en preparación.</p>
      <p>
        Las condiciones de uso y publicación se publicarán cuando la persona responsable, las reglas
        editoriales y la versión definitiva de la licencia estén definidas. Esta página no solicita
        ni registra aceptación de términos.
      </p>
      <p>
        Por ahora puedes consultar las publicaciones públicas y su fuente. La incorporación de
        contenido por la comunidad todavía no está abierta en este sitio.
      </p>
    </template>

    <template v-else>
      <p class="information__lead">
        Queremos una comunidad cultural abierta, respetuosa e inclusiva.
      </p>
      <h2>Cómo participamos</h2>
      <ul>
        <li>Tratamos a las demás personas con empatía y respeto.</li>
        <li>Recibimos los comentarios constructivos con apertura.</li>
        <li>Asumimos los errores, los corregimos y aprendemos de ellos.</li>
        <li>Priorizamos el bienestar colectivo.</li>
      </ul>
      <h2>Conductas que no aceptamos</h2>
      <ul>
        <li>Acoso, ataques personales, insultos o atención no deseada.</li>
        <li>Lenguaje o imágenes sexualizadas en espacios de colaboración.</li>
        <li>Divulgar información privada sin permiso explícito.</li>
        <li>Otras conductas incompatibles con un entorno profesional y seguro.</li>
      </ul>
      <h2>Alcance y aplicación</h2>
      <p>
        El código se aplica en los espacios del proyecto y a quienes lo representan oficialmente. La
        coordinación puede editar o retirar aportaciones contrarias a estas normas. No publiques
        datos personales o evidencia sensible en issues.
      </p>
      <p>
        El texto completo y su atribución están disponibles en el
        <a
          href="https://github.com/Radar-Cultural/radar-community/blob/main/CODE_OF_CONDUCT.md"
          target="_blank"
          rel="noopener noreferrer"
          >repositorio del proyecto</a
        >.
      </p>
    </template>
  </article>
</template>

<style scoped>
.information {
  min-height: 70vh;
  max-width: 56rem;
  padding-block: calc(var(--header) + 4rem) 7rem;
}
.information > a {
  color: var(--text-soft);
  text-decoration: none;
}
.information__eyebrow {
  margin-top: 4rem;
  color: var(--wine);
  font-size: 0.8rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.information h1 {
  margin: 0.5rem 0 2rem;
  font-family: var(--display);
  font-size: clamp(3rem, 7vw, 6rem);
  line-height: 0.98;
  letter-spacing: -0.06em;
}
.information h2 {
  margin-top: 2.5rem;
  font-family: var(--display);
  font-size: 1.6rem;
}
.information p,
.information li {
  font-size: 1.05rem;
  line-height: 1.75;
}
.information__lead {
  font-size: 1.3rem !important;
  font-weight: 650;
}
.information ul {
  padding-left: 1.5rem;
}
.information li + li {
  margin-top: 0.5rem;
}
.information a {
  color: inherit;
}
</style>
