# Contexto para agentes de Radar Community

Este archivo orienta herramientas de IA y personas que colaboren en el repositorio. No sustituye `CONTRIBUTING.md`, `SECURITY.md` ni una decisión registrada en una issue.

## Producto y alcance

Radar Cultural conecta a las personas con eventos, experiencias y espacios culturales mediante difusión gratuita y datos abiertos. Este repositorio contiene Radar Community; Radar Institutional es un producto separado y no debe incorporarse por inferencia.

La fase actual desarrolla `v0.2.0`:

- `frontend/`: landing y futura aplicación pública en Vue 3, Vite y TypeScript.
- `backend/`: Django 5.2, Django REST Framework y PostgreSQL en producción.
- `backend/openapi.yaml`: contrato autoritativo de la API pública.
- `docs/`: arquitectura, API, desarrollo, despliegue y releases.

No inventes eventos, fechas, cifras, alianzas, integrantes, redes sociales, formularios funcionales ni fuentes de datos. Los datos estructurados de eventos sólo se publican a partir de eventos reales y aprobados.

## Invariantes de seguridad

1. La API pública es de sólo lectura. No agregues escrituras públicas sin una issue de arquitectura, permisos por objeto, moderación y pruebas de abuso.
2. Sólo `Event.objects.public()` puede alimentar endpoints públicos. Borradores, contenido oculto y retirado deben responder como inexistentes.
3. Django Admin y futuras escrituras usan sesiones con CSRF. No guardes tokens de larga duración en `localStorage`.
4. No habilites `CORS_ALLOW_ALL_ORIGINS`, comodines en `ALLOWED_HOSTS`, `AllowAny` global ni desactives CSRF.
5. No expongas campos internos como `created_by`, `published_by`, decisiones de moderación, correos, permisos o claves de identidad.
6. Toda consulta de lista debe permanecer paginada y con filtros acotados. Throttling complementa, pero no sustituye, los límites de Nginx/Cloudflare.
7. Los secretos viven fuera de Git. Las variables `VITE_*` son públicas y nunca contienen credenciales.
8. No copies datos, credenciales, OAuth, notificaciones o integraciones de otros proyectos. Luna es una referencia de dominio, no una dependencia.
9. El modelo de usuario personalizado existe desde la migración inicial. No cambies `AUTH_USER_MODEL` después de crear datos.
10. No uses `--fake`, borres migraciones publicadas ni elimines datos para resolver una migración. Prueba cambios con filas heredadas.

## Reglas de diseño

- Identidad: cartografía cultural viva, radar como sistema de conexión y no como decoración genérica.
- Paleta base: `#0d1321`, `#6d4aff`, `#ff5b5b`, `#19b39a`, `#f2f4f7` y acentos vino/dorado sobrios.
- Debe funcionar en tema claro y oscuro, teclado, lector de pantalla, zoom y `prefers-reduced-motion`.
- Mantén HTML y controles como código. No sustituyas UI real con una captura.
- Conserva loaders, estados de foco, hover y error con propósito; evita animación si no explica jerarquía o estado.
- Antes de aprobar una modificación visual, verifica al menos 1440×900, 768×1024 y 390×844.

## Flujo de trabajo

1. Lee la issue y revisa `git status` antes de editar. El trabajo puede ser concurrente: preserva cambios válidos que no sean tuyos.
2. Usa una rama corta. El título del PR sigue Conventional Commits.
3. Cambios funcionales deben cerrar una issue. Cambios de API actualizan primero `backend/openapi.yaml`.
4. No mezcles rediseños, migraciones y refactors no relacionados en un mismo PR.
5. No hagas `git push`, releases, cambios de DNS ni despliegues de producción sin autorización explícita.
6. No uses `git reset --hard` para actualizar producción. El despliegue requiere un árbol limpio y avance `fast-forward`.

## Comandos obligatorios

Frontend:

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm format:check
pnpm lint
pnpm typecheck
pnpm build
```

Backend:

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --requirement requirements-dev.txt
.venv/bin/ruff format --check .
.venv/bin/ruff check .
DEBUG=True .venv/bin/python manage.py check
DEBUG=True .venv/bin/python manage.py makemigrations --check --dry-run
DEBUG=True .venv/bin/python manage.py test
```

Si cambia un modelo, genera la migración de la app afectada, revisa manualmente sus operaciones y pruébala desde una base limpia y, cuando aplique, con datos existentes.

## Evidencia y documentación

- Un build local no prueba navegador, CI ni producción.
- Un test HTTP no prueba el diseño responsive.
- Un servicio activo no prueba el túnel ni el dominio público.
- Reporta por separado: archivos, tests, navegador, GitHub, servidor, Cloudflare y acciones manuales.
- Nunca declares una integración, permiso, etiqueta, issue, PR o despliegue si no observaste su estado real.

## Despliegue

La producción actual sirve el build de Vue mediante Nginx y un túnel dedicado de Cloudflare. El backend aún no está desplegado. Consulta `docs/deployment.md`; no edites unidades systemd, Nginx ni Cloudflare desde una tarea de frontend sin ampliar explícitamente el alcance.
