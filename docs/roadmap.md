# Trabajo pendiente para Community Alpha

Este documento registra unidades reales de trabajo para convertirlas en issues de GitHub cuando la cuenta conectada tenga acceso al repositorio. No sustituye las issues ni asigna números inexistentes.

La decisión de convertir Radar en fuente principal también de preferencias, favoritos,
asistencia, recordatorios y notificaciones introduce trabajo posterior a la API pública de
lectura. El inventario, el orden y los criterios para abrir issues están en
[Radar como API central: brechas frente a Luna](radar-api-central-gap.md).

## `feat: completar administración y revisión de eventos`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: feature`, `area: backend`, `priority: high`, `status: in progress`.
- Implementado localmente: la verificación de organizaciones requiere `verify_organization` y fija la autoría desde la sesión; el permiso general de edición no permite verificar ni revocar. Los eventos deben pasar de borrador a revisión antes de publicarse; cada transición administrativa queda en una bitácora de sólo lectura. Dos pruebas HTTP del formulario real confirman CSRF, rechazo del salto directo a publicado, publicación desde revisión y bloqueo de POST para personal sin `publish_event`.
- Terminado cuando el personal autorizado puede crear, revisar y publicar desde Django Admin; las transiciones quedan auditadas; y borradores, ocultos y retirados continúan fuera de la API pública.

## `test: validar modelos y migraciones en PostgreSQL`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: enhancement`, `area: backend`, `priority: high`, `status: in progress`.
- Verificado localmente en PostgreSQL 18.6: migraciones desde cero y 70 pruebas del backend (dos pruebas del comando DEMO se omiten por su restricción deliberada a SQLite). La suite SQLite actual pasó 81 pruebas, incluidas dos pruebas HTTP del flujo administrativo. Bases temporales con datos heredados conservaron un evento publicado, lugares, alias, categorías, públicos y una organización; las migraciones recalcularon identidades Unicode y completaron slugs vacíos sin inventar historial editorial. El filtro de eventos aún vigentes y la actualización del cursor por cambios relacionados pasaron en SQLite y PostgreSQL. Cuatro pruebas nuevas o modificadas sobre actividad en curso sin fecha final, moneda obligatoria y publicación por Admin pasaron también en un PostgreSQL 18.6 temporal y aislado. Las últimas pruebas de iCalendar, encabezado Host, filtrado de claves JSON y revocación de organización sólo se ejecutaron en SQLite.
- Preparado localmente: CI con PostgreSQL 17 para migraciones y suite. El gate de despliegue ahora permite únicamente los avisos HSTS `security.W005` y `security.W021` diferidos por política, y falla con cualquier aviso o error nuevo; se verificó con la configuración de CI y una prueba de rechazo. Todavía no hay una ejecución de GitHub Actions observada para estos cambios sin commit.
- Falta: repetir la verificación en la versión y configuración de PostgreSQL elegidas para producción antes del despliegue.
- Terminado cuando migraciones, restricciones, índices y pruebas pasan en una versión soportada de PostgreSQL con datos heredados representativos y sin usar `--fake`.

## `feat: consumir la agenda pública desde Vue`

- Milestone propuesto: `v0.2.0 — Community Alpha`.
- Etiquetas: `type: feature`, `area: frontend`, `area: api`, `priority: medium`, `status: in progress`.
- Implementado localmente: cliente TypeScript de mismo origen, `/agenda/` con búsqueda y paginación, ficha HTML de Django con estado HTTP y Schema.org, sitemap público, estados accesibles de carga, vacío y error, y selección de hasta cuatro eventos de una página aleatoria de próximos eventos con imagen reutilizable en el hero. La zona IANA se valida para publicaciones nuevas; los registros heredados sin zona se muestran como UTC. Los lugares requieren un país explícito y se distinguen por región y país, incluso si comparten nombre y alias.
- Los nombres no latinos conservan su identidad en lugares y alias; categorías, públicos y organizaciones reciben slugs ASCII estables si el nombre no puede transliterarse. Los filtros públicos de slugs, UUID y fechas tienen límites de longitud explícitos.
- La respuesta y la ficha Schema.org omiten afirmaciones de disponibilidad de entradas que no se han verificado; un permiso registrado sin licencia pública devuelve `license_url: null` en lugar de enlazar a una licencia inexistente.
- La agenda y el hero incluyen eventos que siguen en curso o tienen actividades futuras, y filtran cancelados en su vista principal; `from` conserva su semántica de fecha de inicio para consumidores existentes.
- El filtro también contempla una actividad que ya empezó y todavía no termina aunque el evento no tenga fecha final. Una entrada con costo exige moneda explícita y precio finito; no se infiere MXN.
- Tres eventos ficticios y rotulados DEMO se generan sólo con `DEBUG=True` y SQLite local. El hero, la agenda, la búsqueda y la ficha HTML se verificaron conectados a Django mediante el proxy de Vite en `127.0.0.1:5174` → `127.0.0.1:8002`; ninguna de esas publicaciones pertenece a producción.
- La ficha HTML usa la misma marca, navegación y control de tema que la agenda. En el hero, los créditos breves caben en las tarjetas y el cuarto fragmento editorial usa una imagen distinta de las tres muestras. El recorrido hero → agenda → búsqueda y hero → ficha pasó en navegador local; el menú y el tema de la ficha se comprobaron en 1440×900, 768×1024 y 390×844, sin desbordamiento horizontal.
- Los títulos y textos editoriales de cada evento llevan su etiqueta de idioma cuando está verificada, también en las vistas Vue, para facilitar pronunciación correcta por lectores de pantalla.
- Las opciones de entrada y los enlaces se reducen a campos públicos explícitos aun si una importación heredada guardó claves adicionales; la prueba comprueba que un token y correo internos no aparecen en lista, detalle JSON, Schema.org, RDF/XML ni ficha HTML. Un precio no finito o una URL inválida heredados se omiten; una ficha con todas las opciones inválidas permanece disponible y remite a la fuente para consultar entradas.
- Toda la API v1 devuelve `Cache-Control: no-store`; la prueba de revocación comprueba que una organización desverificada desaparece del detalle y la lista con ese encabezado, también en la respuesta `404`.
- La colección Postman se ejecutó contra una instancia local temporal de Django con los tres eventos DEMO: 10 solicitudes y 25 aserciones pasaron; la instancia se cerró después de la prueba. Esto no verifica el dominio público ni GitHub Actions.
- La ficha HTML presenta programa, públicos, enlaces, país y opciones de entrada con precio y moneda. Se verificó con un taller mixto DEMO en `Europe/Paris`, precio en EUR y revisión visual de 1440×900, 768×1024 y 390×844; el panel pasa a una columna en tableta para conservar legibilidad.
- Verificación local con datos temporales: navegación del hero a ficha HTML, agenda y búsqueda, selección de eventos entre varias páginas, horarios de cuatro zonas internacionales y revisión visual de 1440×900, 768×1024 y 390×844. Otra revisión comprobó cuatro eventos con imagen en el hero, la acción hacia la agenda, el evento en curso visible y el cancelado ausente. Esos datos temporales se eliminaron al terminar y no representan publicaciones reales.
- Falta: validar el flujo con publicaciones reales aprobadas y probar las rutas, metadatos y retirada tras desplegar la API.
- Terminado cuando existen eventos reales verificables, las fichas responden con estado HTTP y metadatos correctos, y pasan pruebas responsive y de accesibilidad con datos reales.

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
- Ejecutar la migración gradual de Luna con UUID remoto, cursor incremental, tolerancia a fallos y rollback; no activar el corte hasta que Radar esté desplegado y tenga datos reales verificados.
