# Arquitectura

## Visión general

```text
Navegador
  ├─ /                → Nginx → build Vue
  └─ /api/v1/         → Nginx → Gunicorn → Django REST Framework → PostgreSQL
                                  └─ /admin/ protegido por sesión y CSRF

Internet → Cloudflare → túnel dedicado → Nginx local
```

El frontend y la API comparten origen público. En desarrollo, Vite usa un proxy local para `/api`; no se habilita CORS comodín.

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

## Límites actuales

- No existe escritura pública ni autenticación de clientes externos.
- Django Admin es la única superficie inicial de gestión.
- No se implementan recordatorios, calendario, notificaciones, tickets ni analítica.
- No se despliega el backend hasta preparar PostgreSQL, servicio Gunicorn, proxy Nginx, variables y respaldo.
