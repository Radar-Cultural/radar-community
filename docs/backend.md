# Backend

## Objetivo

El backend inicia la base de datos cultural canónica de Radar Community con Django REST Framework. Toma como referencia conceptos probados en Luna —catálogos, lugares normalizados, fuentes, licencias, publicación y moderación— sin copiar su dominio académico, personalización de tarjetas ni credenciales de integraciones personales.

## Aplicaciones

| App | Responsabilidad |
|---|---|
| `accounts` | Usuario UUID y organizaciones verificables. |
| `catalog` | Categorías, públicos, lugares jerárquicos y alias normalizados. |
| `events` | Eventos, horarios, contribuidores y aceptación de publicación. |
| `moderation` | Reportes y decisiones auditables. |
| `api` | Serialización pública, filtros, paginación y contrato HTTP. |

## Frontera pública

La API `v1` sólo permite `GET`, `HEAD` y `OPTIONS`. La creación y revisión se hace inicialmente en Django Admin por personal autenticado. Esto evita abrir escrituras antes de definir verificación de identidad, permisos por objeto, moderación y protección contra abuso.

La consulta pública usa exclusivamente `Event.objects.public()`. No expone borradores, contenido oculto, contenido retirado, autores internos ni decisiones de moderación.

La API también entrega sincronización incremental por `updated_since`, orden estable, agenda interna, opciones de admisión, vínculos verificables e imagen únicamente cuando existe una licencia reutilizable. JSON-LD, RDF/XML e iCalendar se generan desde la misma publicación pública para evitar divergencias.
La ficha HTML de Django presenta el programa, públicos, enlaces, ubicación con país y opciones de
entrada con precio y moneda cuando están publicados. La página usa la zona IANA del evento para
mostrar fechas y horarios; la interfaz de navegación permanece en español.

La moderación se aplica mediante una operación transaccional: exige el permiso `review_content_reports`, bloquea el reporte y el evento mientras cambia su estado, asigna responsable y conserva visibilidad anterior, visibilidad nueva, motivo y marca temporal. Las decisiones guardadas son inmutables desde Django Admin.

En Django Admin, `created_by` se fija a la persona autenticada al crear un evento y `published_by` a quien lo publica. Ambos campos y `visibility_status` son de sólo lectura; las acciones de visibilidad pasan por moderación. Editar o despublicar un evento ya publicado exige `publish_event`. El estado, la asignación y la autoría de un reporte tampoco se modifican desde su formulario: las transiciones se registran mediante decisiones de moderación.

Los eventos se crean como borradores y avanzan por `draft → in_review → published`. Desde revisión se puede devolver a borrador; una publicación puede volver a revisión o archivarse; un archivo puede regresar a borrador. Enviar un borrador a revisión no requiere un permiso editorial extra, devolverlo desde revisión requiere `review_event` y publicar, editar o retirar una publicación requiere `publish_event`. Cada cambio de estado administrativo guarda actor, estado anterior, estado nuevo y fecha en `EventPublicationDecision`. La bitácora es de sólo lectura en Admin y no se permite borrar eventos desde esa interfaz.

La verificación y revocación de organizaciones exigen el permiso `verify_organization`, además del acceso administrativo normal. El actor y la fecha de verificación se fijan desde la sesión y son de sólo lectura; la cuenta propietaria de una organización no puede sustituirse al editarla.

## Autenticación

- Admin y futuras operaciones del navegador: sesión segura y CSRF.
- API pública: lectura anónima con throttling y paginación.
- OAuth/OIDC o credenciales para integraciones se decidirán mediante ADR/issue antes de exponer escrituras.
- No se usa Basic Auth ni se entregan tokens permanentes al frontend.

## Base de datos

SQLite se permite para desarrollo y CI. Producción exige PostgreSQL mediante `DATABASE_URL`. Las ubicaciones usan identidad estable, jerarquía y coordenadas; el código de país es explícito y la clave de identidad incluye región y país para no mezclar recintos homónimos en distintos territorios. La normalización conserva escrituras no latinas y los slugs de categorías, públicos y organizaciones reciben un identificador ASCII estable cuando el nombre no puede transliterarse. Los alias de búsqueda pueden repetirse entre recintos, pero no dentro de uno mismo. Los eventos conservan fuente verificable, estado Schema.org y estado interno de publicación por separado.

## Seguridad

- `DEBUG=False` y secretos obligatorios en producción.
- Hosts y orígenes CSRF explícitos.
- HTTPS, cookies seguras, HSTS, `X-Frame-Options` y `nosniff`.
- Sin CORS comodín; desarrollo usa proxy de Vite.
- JSON como único renderer de la API pública.
- Las representaciones semánticas e iCalendar usan vistas explícitas y de sólo lectura; no amplían los renderers globales de DRF.
- Límite de 100 resultados por página y consultas textuales de hasta 120 caracteres.
- Los filtros temporales requieren zona horaria explícita para no interpretar fechas internacionales como hora de México.
- Nginx/Cloudflare deben aplicar límites adicionales; el throttling de DRF no es protección DDoS.
