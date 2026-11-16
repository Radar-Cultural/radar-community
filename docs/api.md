# API pública

El contrato autoritativo está en [`backend/openapi.yaml`](../backend/openapi.yaml). La implementación inicial vive bajo `/api/v1/`.
Las URL absolutas se generan desde el encabezado `Host` validado por Django; el proxy no debe reenviar valores de `X-Forwarded-Host` proporcionados por clientes.

## Endpoints

| Método | Ruta | Acceso |
|---|---|---|
| `GET` | `/api/v1/status/` | Público; estado mínimo. |
| `GET` | `/api/v1/events/` | Público; sólo publicaciones visibles. |
| `GET` | `/api/v1/events/{slug}/` | Público; un evento visible. |
| `GET` | `/api/v1/events/{slug}/schema/` | Público; JSON-LD Schema.org. |
| `GET` | `/api/v1/events/{slug}/schema.rdf` | Público; RDF/XML Schema.org. |
| `GET` | `/api/v1/events/{slug}/calendar.ics` | Público; exportación iCalendar. |
| `GET` | `/api/v1/categories/` | Público; catálogo activo. |
| `GET` | `/api/v1/audiences/` | Público; catálogo activo. |
| `GET` | `/api/v1/places/` | Público; lugares activos. |
| `GET` | `/api/v1/places/{id}/` | Público; un lugar activo. |
| `GET` | `/api/v1/organizations/` | Público; organizaciones verificadas. |
| `GET` | `/api/v1/organizations/{slug}/` | Público; una organización verificada. |

## Consultas de eventos

- `q`: título, resumen y descripción; máximo 120 caracteres.
- `category`, `audience`: slug ASCII del catálogo, hasta 180 caracteres.
- `place`: UUID del lugar, hasta 36 caracteres.
- `from`, `to`: fecha y hora ISO 8601 con zona horaria explícita (`Z` u offset), hasta 64 caracteres. Si se envían ambas, `to` debe ser igual o posterior a `from`.
- `not_finished_at`: próximos eventos y eventos en curso en el instante indicado; usa el fin del evento y los inicios o finales de las actividades del programa cuando existen. Se puede combinar con los otros filtros.
- `updated_since`: cambios desde una fecha y hora ISO 8601 con zona horaria explícita, hasta 64 caracteres; base de la sincronización de consumidores. El cursor también avanza con ediciones normales de horarios, categorías, públicos, lugares y organizaciones relacionadas.
- `organizer`: slug ASCII de una organización verificada, hasta 280 caracteres. El filtro no permite descubrir asociaciones con perfiles todavía no verificados.
- `status`, `attendance_mode`: valores acotados por el contrato.
- `ordering`: `starts_at`, `-starts_at`, `updated_at` o `-updated_at`.
- `page`, `page_size`: paginación; máximo 100.
- `has_image=true|false`: eventos con o sin imagen reutilizable visible en la respuesta pública.

Una publicación inexistente, en borrador, oculta o retirada responde `404`; no se revela cuál de esos estados tiene.
Las opciones de entrada y los enlaces de cada evento se serializan mediante una lista explícita de claves públicas. La respuesta JSON, Schema.org, RDF/XML y la ficha HTML omiten claves adicionales y valores anidados inválidos de registros importados o heredados.
Todas las respuestas de `/api/v1/`, la ficha HTML de eventos y los mapas dinámicos llevan `Cache-Control: no-store`. Así, un navegador o intermediario que respete HTTP no conserva una copia pública tras la retirada de un evento, categoría, lugar u organización. Esto no sustituye la revisión de reglas de caché de Nginx y Cloudflare antes del despliegue.

La ficha pública `/eventos/{slug}/` la sirve Django como HTML con metadatos y JSON-LD en la respuesta inicial. La propiedad `url` de Schema.org apunta a esa ficha, mientras `/api/v1/events/{slug}/` sigue siendo la representación JSON para consumidores. La ficha y la API comparten el mismo filtro de publicación; no se genera HTML indexable para borradores o eventos retirados.
El archivo iCalendar escapa separadores y saltos de línea del contenido editorial, normaliza retornos de carro y pliega líneas UTF-8 a un máximo de 75 octetos por línea física conforme a [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545.html). La ubicación incluye recinto, detalles, localidad, región y país cuando existen; un evento híbrido también incluye su acceso en línea en la descripción. Conserva el UUID del evento en `UID` para que los clientes puedan reconocer actualizaciones.

`/sitemap.xml` es un índice que enlaza los mapas de páginas estáticas y de eventos. El mapa de eventos se pagina y consulta exclusivamente `Event.objects.public()`; las páginas legales pendientes de revisión no se incluyen. `robots.txt` anuncia el índice.

Cada evento puede indicar `language_code` con una etiqueta como `es-MX`, `en-US` o `zh-Hant-TW`. Si el idioma no se ha verificado, devuelve `null` y Schema.org omite `inLanguage`. Una entrada gratuita no declara una moneda ficticia; las entradas con costo conservan la moneda explícita de cada opción.
Las opciones con costo exigen una moneda explícita de tres letras ASCII y un precio finito no negativo; no se infiere `MXN` a partir del servidor o del idioma.

`license_url` sólo contiene una URL para licencias públicas identificadas. Con `description_license=permission-recorded` devuelve `null` y Schema.org omite `license`, porque un permiso registrado no define una licencia pública reutilizable. Las ofertas omiten `availability`: la agenda no verifica inventario de entradas.

`time_zone` identifica la zona IANA verificada del horario (`Europe/Paris`, `America/Mexico_City`, etcétera). Es obligatoria para nuevas publicaciones. Los registros heredados sin zona comprobada conservan `null`; sus instantes siguen siendo UTC y se muestran explícitamente como UTC, sin atribuirles una zona local inventada. `startDate` y `endDate` de Schema.org usan el offset de la zona del evento cuando se conoce.

Los consumidores deben guardar el `id` UUID de Radar como identidad remota, tratar `updated_at` como cursor de cambio y volver a consultar cuando el evento sea cancelado o reprogramado. La desaparición de un UUID antes conocido requiere despublicarlo localmente, no conservar una copia pública obsoleta.

Las importaciones y correcciones masivas deben actualizar expresamente `Event.updated_at` de los
eventos afectados: `QuerySet.update()` y SQL directo omiten las señales de Django que mantienen
el cursor de los cambios relacionados.

Por ejemplo, `2026-11-08T12:00:00Z` y `2026-11-08T07:00:00-05:00` representan el mismo instante. Una hora sin zona se rechaza con `400` para que clientes de otros países no reciban resultados desplazados por la zona configurada en el servidor.

La preparación específica para Luna está en [`luna-integration.md`](luna-integration.md).

## Cambiar el contrato

1. Abrir una issue que describa consumidor, compatibilidad y permisos.
2. Modificar primero `backend/openapi.yaml`.
3. Agregar o ajustar pruebas de respuestas y errores.
4. Implementar el cambio sin ampliar campos internos.
5. Generar/actualizar la colección Postman desde el OpenAPI.
6. Solicitar revisión de CODEOWNERS.

Los cambios incompatibles no se incorporan silenciosamente a `v1`; requieren una estrategia de versión.

## Colección Postman local

La colección Git-native en `postman/collections/Radar Cultural API/` se genera desde el contrato y conserva aserciones compartidas. No contiene tokens ni secretos.

Validación estructural:

```bash
postman spec lint backend/openapi.yaml --fail-severity warning --no-report-events
postman collection lint "postman/collections/Radar Cultural API"
```

Ejecución contra un backend local ya iniciado y con los tres eventos de `seed_demo_events` en SQLite de desarrollo:

```bash
postman collection run "postman/collections/Radar Cultural API" \
  --env-var baseUrl=http://127.0.0.1:8002/api/v1 \
  --env-var eventSlug=demo-danza \
  --no-report-events \
  --timeout-request 5000
```

El valor predeterminado de `baseUrl` apunta a localhost; se puede reemplazar con `--env-var` para usar otro puerto. No ejecutes la colección contra el dominio público hasta que el backend se publique y verifique.
