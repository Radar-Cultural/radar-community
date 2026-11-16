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
La única excepción para pruebas locales es `manage.py seed_demo_events`: genera tres registros
ficticios rotulados DEMO en SQLite con `DEBUG=True`. No se despliegan, sincronizan con Luna ni se
presentan como programación real.

## Radar como motor central: decisión y trabajo pendiente

Radar Cultural será la fuente canónica del catálogo cultural **y** de favoritos, preferencias de
descubrimiento, asistencia, recordatorios y notificaciones de las personas usuarias. Luna y las
próximas agendas serán clientes; no deben crear una segunda autoridad para esos datos. La
personalización visual de tarjetas de Luna no se traslada a Radar.

Esto es una **decisión de arquitectura, no una función ya implementada**. Hoy Radar sólo expone
lecturas públicas de eventos y catálogos; Django Admin gestiona publicaciones. Faltan identidad
compartida y autenticación de clientes, modelos y endpoints privados con permisos por persona,
flujo de contribución revisada, entrega de recordatorios y notificaciones, y sincronización de
retiradas para consumidores. El inventario, las dependencias y los criterios de aceptación están
en `docs/radar-api-central-gap.md`; `docs/luna-integration.md` describe el puente de consumo.
Actualiza ambos documentos, `backend/openapi.yaml`, las pruebas y la documentación de privacidad
antes de implementar cada capacidad. No copies cuentas,
credenciales, tokens OAuth, suscripciones push ni datos personales de Luna.

## Invariantes de seguridad

1. El catálogo público y anónimo es de sólo lectura. Las futuras operaciones privadas de personas y organizaciones requieren autenticación, una issue de arquitectura, permisos por objeto, moderación cuando corresponda y pruebas de abuso; nunca abras escrituras anónimas por inferencia.
2. Sólo `Event.objects.public()` puede alimentar endpoints públicos. Borradores, contenido oculto y retirado deben responder como inexistentes.
3. Django Admin y las futuras escrituras desde navegadores con sesión usan CSRF. La autenticación de clientes externos requiere una decisión y pruebas propias. No guardes tokens de larga duración en `localStorage`.
4. No habilites `CORS_ALLOW_ALL_ORIGINS`, comodines en `ALLOWED_HOSTS`, `AllowAny` global ni desactives CSRF.
5. No expongas campos internos como `created_by`, `published_by`, decisiones de moderación, correos, permisos o claves de identidad.
6. Toda consulta de lista debe permanecer paginada y con filtros acotados. Throttling complementa, pero no sustituye, los límites de Nginx/Cloudflare.
7. Los secretos viven fuera de Git. Las variables `VITE_*` son públicas y nunca contienen credenciales.
8. No copies datos, credenciales, OAuth, notificaciones o integraciones de otros proyectos. Luna es una referencia de dominio, no una dependencia.
9. El modelo de usuario personalizado existe desde la migración inicial. No cambies `AUTH_USER_MODEL` después de crear datos.
10. No uses `--fake`, borres migraciones publicadas ni elimines datos para resolver una migración. Prueba cambios con filas heredadas.

## Reglas de diseño

- Identidad: cartografía cultural viva, radar como sistema de conexión y no como decoración genérica.
- Dirección vigente: “cartografía cultural viva”. El hero centra la marca y la rodea con fragmentos editoriales de distintas prácticas culturales; al desplazarse, las imágenes caen, se separan, pierden nitidez y entregan el protagonismo al relato. La propuesta se explica como punto, ruta y red.
- Los símbolos de libro, música, escena, cine y artes visuales pueden funcionar como máscaras tipográficas o geometría narrativa, no como una cuadrícula genérica de iconos.
- El radar se reserva para el cierre y debe aparecer incompleto, recortado por el borde de la pantalla. No repitas radares ni uses interfaces de ciencia ficción.
- Paleta vigente: tinta `#08090d`, blanco `#f7f8fa`, señal `#3157ff`, vino `#6b1536` y coral `#ff5a4f` como acento contenido.
- Debe funcionar en tema claro y oscuro, teclado, lector de pantalla, zoom y `prefers-reduced-motion`.
- Mantén HTML y controles como código. No sustituyas UI real con una captura.
- Conserva loaders, estados de foco, hover y error con propósito; evita animación si no explica jerarquía o estado.
- Antes de aprobar una modificación visual, verifica al menos 1440×900, 768×1024 y 390×844.

## Flujo de trabajo

1. Lee la issue y revisa `git status` antes de editar. El trabajo puede ser concurrente: preserva cambios válidos que no sean tuyos.
2. Usa una rama corta con prefijo `feature/`, `fix/`, `update/`, `docs/`, `test/`, `ci/` o `refactor/` seguido de un slug. La barra separa el tipo en ramas; los dos puntos corresponden a títulos Conventional Commits de PR/commit (`feat:`, `fix:`, etc.). `update/` identifica mantenimiento de contenido o dependencias sin cambio funcional; su título de PR usa `chore:` o `docs:` según el caso.
3. Cambios funcionales deben cerrar una issue. Cambios de API actualizan primero `backend/openapi.yaml`.
4. No mezcles rediseños, migraciones y refactors no relacionados en un mismo PR.
5. No hagas `git push`, releases, cambios de DNS ni despliegues de producción sin autorización explícita.
6. No uses `git reset --hard` para actualizar producción. El despliegue requiere un árbol limpio y avance `fast-forward`.
7. No crees, enmiendes, combines ni reescribas commits hasta que el propietario revise los cambios sin commit y autorice explícitamente confirmarlos.

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
