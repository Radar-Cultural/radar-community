# Arquitectura

## Visión general

```text
Navegador
  ├─ /                → Nginx → build Vue
  └─ /api/v1/         → Nginx → Gunicorn → Django REST Framework → PostgreSQL
                                  └─ /admin/ protegido por sesión y CSRF

Internet → Cloudflare → túnel dedicado → Nginx local
```

El frontend y la API comparten origen público. En desarrollo, Vite usa un proxy local para `/api`; no se habilita CORS comodín. Radar Cultural es la fuente canónica de publicaciones culturales y, como objetivo aún no implementado, de preferencias culturales, favoritos, asistencia, recordatorios y notificaciones. Luna y otras agendas consumirán estas funciones mediante identidad y permisos definidos, usando el UUID estable de Radar en lugar de duplicar la ficha cultural. Consulta [las brechas frente a Luna](radar-api-central-gap.md).

## Frontend

Vue compone una landing accesible con tema claro/oscuro, movimiento reducido, componentes semánticos y recursos optimizados por Vite. El frontend no contiene secretos ni simula llamadas a servicios inexistentes.

## Backend

Django conserva por separado:

- estado cultural de un evento (`EventScheduled`, cancelado, pospuesto o reprogramado);
- estado editorial (`draft`, revisión, publicado o archivado);
- visibilidad de moderación (público, oculto o retirado).

Esta separación evita publicar un borrador o confundir cancelación con retirada. Los eventos públicos requieren fuente verificable y sólo salen de `Event.objects.public()`.

Los catálogos normalizan lugares y alias con identidad estable. Organización, evento y lugar tienen UUID; los slugs son rutas legibles, no identificadores internos.

## Contrato

`backend/openapi.yaml` es la fuente autoritativa. La implementación, las pruebas y la colección Postman deben derivarse o contrastarse contra ese archivo. Los cambios incompatibles requieren versión nueva.

Cada evento publicado ofrece tres representaciones complementarias: JSON de la API para aplicaciones, JSON-LD/RDF/XML con vocabulario Schema.org para interoperabilidad y un archivo iCalendar para exportación. Todas nacen del mismo evento filtrado por `Event.objects.public()`.

## Límites actuales

- No existe escritura pública ni autenticación de clientes externos.
- Django Admin es la única superficie inicial de gestión.
- Radar exporta iCalendar, pero todavía no conserva conexiones de calendario, tokens OAuth, favoritos, asistencia, recordatorios, notificaciones ni preferencias personales. Los datos personales compartidos pasarán a Radar sólo después de diseñar identidad, permisos, consentimiento y API privada; no se copiarán credenciales de Luna.
- No se implementan tickets ni analítica de personas.
- No se despliega el backend hasta preparar PostgreSQL, servicio Gunicorn, proxy Nginx, variables y respaldo.
