# Despliegue

## Flujo GitHub → Vercel

La integración oficial de Vercel observa el repositorio de GitHub. La configuración objetivo es:

| Campo | Valor |
|---|---|
| Project Name | `radar-community` |
| Framework Preset | Vite |
| Root Directory | `frontend` |
| Package Manager | pnpm |
| Install Command | `pnpm install --frozen-lockfile` |
| Build Command | `pnpm build` |
| Output Directory | `dist` |
| Production Branch | `main` |

Un pull request crea un Preview Deployment. Un push aceptado a `main` crea un Production Deployment. No existe un segundo pipeline por tags: GitHub Releases documenta versiones y Vercel publica desde `main`.

## Verificación de una publicación

1. Confirma que CI terminó correctamente para el commit.
2. Abre el deployment asociado a ese mismo SHA en Vercel.
3. Comprueba que el estado sea `Ready` y que el build use `frontend/`.
4. Abre la URL y valida título, contenido, consola, assets y responsive.
5. Comprueba el estado de Vercel dentro del commit o pull request de GitHub.
6. En producción, verifica también `https://radarcultural.mx` y el comportamiento de `www`.

Un build local o un estado `Ready` no sustituye la comprobación de la URL publicada.

## Volver a una versión anterior

Desde Vercel, localiza un deployment de producción previamente verificado y usa **Promote to Production**. Esto reasigna los dominios al artefacto existente y evita reconstruir un commit distinto. Después verifica la URL pública y registra la razón del rollback.

No reescribas tags publicados para representar un rollback. Si el código necesita una corrección, crea una nueva versión, por ejemplo `v0.1.1`.

## Dominio

El dominio objetivo es `radarcultural.mx`; `www.radarcultural.mx` debe redirigir al dominio principal. Antes de cambiar DNS:

1. Inspecciona los registros actuales y los servicios que dependen de ellos.
2. Agrega el dominio al proyecto de Vercel y utiliza exactamente los registros que Vercel solicite.
3. Si DNS se administra en Cloudflare, conserva correo y otros registros no relacionados.
4. Verifica propiedad, certificado TLS y redirección de `www`.
5. No elimines registros existentes sin una evaluación explícita.

Hasta completar esa verificación, utiliza la URL temporal `*.vercel.app` y no declares activo el dominio personalizado.

