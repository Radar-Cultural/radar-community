# API pública

El contrato autoritativo está en [`backend/openapi.yaml`](../backend/openapi.yaml). La implementación inicial vive bajo `/api/v1/`.

## Endpoints

| Método | Ruta | Acceso |
|---|---|---|
| `GET` | `/api/v1/status/` | Público; estado mínimo. |
| `GET` | `/api/v1/events/` | Público; sólo publicaciones visibles. |
| `GET` | `/api/v1/events/{slug}/` | Público; un evento visible. |
| `GET` | `/api/v1/categories/` | Público; catálogo activo. |
| `GET` | `/api/v1/audiences/` | Público; catálogo activo. |
| `GET` | `/api/v1/places/` | Público; lugares activos. |

## Consultas de eventos

- `q`: título, resumen y descripción; máximo 120 caracteres.
- `category`, `audience`: slug del catálogo.
- `place`: UUID del lugar.
- `from`, `to`: fecha y hora ISO 8601.
- `page`, `page_size`: paginación; máximo 100.

Una publicación inexistente, en borrador, oculta o retirada responde `404`; no se revela cuál de esos estados tiene.

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

Ejecución contra un backend local ya iniciado y con el fixture `evento-de-prueba` en una base desechable:

```bash
postman collection run "postman/collections/Radar Cultural API" \
  --env-var baseUrl=http://127.0.0.1:8000/api/v1 \
  --no-report-events \
  --timeout-request 5000
```

El valor persistente de `baseUrl` apunta a producción, pero la API aún no está desplegada; no ejecutes la colección contra el dominio público hasta que el backend se publique y verifique.
