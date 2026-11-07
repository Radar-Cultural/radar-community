# Trabajo pendiente para Community Alpha

Este documento registra unidades reales de trabajo para convertirlas en issues de GitHub cuando la cuenta conectada tenga acceso al repositorio. No sustituye las issues ni asigna números inexistentes.

## `feat: completar administración y revisión de eventos`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: feature`, `area: backend`, `priority: high`, `status: ready`.
- Terminado cuando el personal autorizado puede crear, revisar y publicar desde Django Admin; las transiciones quedan auditadas; y borradores, ocultos y retirados continúan fuera de la API pública.

## `test: validar modelos y migraciones en PostgreSQL`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: enhancement`, `area: backend`, `priority: high`, `status: ready`.
- Terminado cuando migraciones, restricciones, índices y pruebas pasan en una versión soportada de PostgreSQL con datos heredados representativos y sin usar `--fake`.

## `feat: consumir la agenda pública desde Vue`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: feature`, `area: frontend`, `area: api`, `priority: medium`, `status: blocked`.
- Bloqueo real: requiere fuentes y publicaciones verificadas; no se usarán eventos ficticios para simular la experiencia.
- Terminado cuando existen estados accesibles de carga, vacío y error, filtros acotados y pruebas responsive.

## `chore: desplegar API con PostgreSQL y Gunicorn`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `area: devops`, `area: backend`, `priority: high`, `status: blocked`.
- Bloqueo real: requiere autorización de producción, respaldo, variables, base dedicada, unidad systemd y configuración Nginx revisada.
- Terminado cuando el servicio aislado está sano, las migraciones y archivos estáticos están aplicados, `/api/v1/status/` responde por el dominio y las escrituras públicas continúan cerradas.

## `test: auditoría de seguridad y accesibilidad de la alpha`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: security`, `area: accessibility`, `priority: high`, `status: blocked`.
- Bloqueo real: requiere una alpha desplegada.
- Terminado cuando se revisan permisos por objeto, CSRF, cabeceras, abuso, fuga de campos, teclado, lector de pantalla, contraste, zoom, movimiento reducido y viewports acordados.

## Decisiones previas a `v1.0.0`

- Aprobar licencia definitiva antes de presentar el repositorio como open source.
- Definir identidad y permisos de organizaciones antes de abrir escrituras por API.
- Definir retención, corrección y retiro de datos culturales con participación de la comunidad.
