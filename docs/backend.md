# Backend

## Objetivo

El backend inicia la base de datos cultural de Radar Community con Django REST Framework. Toma como referencia conceptos probados en Luna —catálogos, lugares normalizados, fuentes, licencias, publicación y moderación— sin copiar su dominio académico ni sus integraciones.

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

## Autenticación

- Admin y futuras operaciones del navegador: sesión segura y CSRF.
- API pública: lectura anónima con throttling y paginación.
- OAuth/OIDC o credenciales para integraciones se decidirán mediante ADR/issue antes de exponer escrituras.
- No se usa Basic Auth ni se entregan tokens permanentes al frontend.

## Base de datos

SQLite se permite para desarrollo y CI. Producción exige PostgreSQL mediante `DATABASE_URL`. Las ubicaciones usan identidad estable, jerarquía y coordenadas; los eventos conservan fuente verificable, estado Schema.org y estado interno de publicación por separado.

## Seguridad

- `DEBUG=False` y secretos obligatorios en producción.
- Hosts y orígenes CSRF explícitos.
- HTTPS, cookies seguras, HSTS, `X-Frame-Options` y `nosniff`.
- Sin CORS comodín; desarrollo usa proxy de Vite.
- JSON como único renderer de la API pública.
- Límite de 100 resultados por página y consultas textuales de hasta 120 caracteres.
- Nginx/Cloudflare deben aplicar límites adicionales; el throttling de DRF no es protección DDoS.
