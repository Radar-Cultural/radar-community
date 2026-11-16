# Integración futura de Luna

## Frontera de responsabilidades

Radar Cultural será la fuente canónica de categorías, públicos, lugares, organizaciones, eventos, horarios, licencias y estado editorial público. Por decisión del propietario, también será la fuente principal de preferencias culturales, favoritos, asistencia, notificaciones y recordatorios. Luna será un consumidor de esos datos y conservará únicamente funciones propias de su presentación y contexto académico. La identidad compartida y las operaciones privadas todavía no están implementadas; el inventario de brechas está en [Radar como API central](radar-api-central-gap.md).

No se copia a Radar la personalización visual de tarjetas ni se trasladan tokens OAuth, suscripciones push o historiales personales desde la base de Luna. Si Radar ofrece esos canales en el futuro, necesitará consentimiento y conexiones propias. Tampoco se importan automáticamente eventos actuales: cada publicación necesita fuente y revisión.

## Identidad y sincronización

1. Luna agrega a su evento consumido un `radar_event_id` UUID único y un `radar_updated_at`.
2. La carga inicial recorre `/api/v1/events/` con paginación.
3. Las cargas siguientes consultan `updated_since`, ordenadas por `updated_at` y con un pequeño solapamiento temporal para evitar perder cambios en el límite.
   Las ediciones de horario, categorías, públicos, lugar y organización hechas mediante los modelos
   de Django actualizan el cursor del evento. Cargas masivas con `QuerySet.update()` o SQL directo
   deben tocar `Event.updated_at` de los eventos afectados.
4. La importación es idempotente por `radar_event_id`; no usa título, slug ni URL como identidad.
5. Una cancelación o reprogramación actualiza la ficha y los recordatorios gestionados por Radar según el consentimiento vigente; Luna muestra el estado recibido.
6. Si un evento antes conocido deja de estar disponible, Luna lo retira de descubrimiento y conserva sólo la caché mínima necesaria para continuidad. Las relaciones privadas siguen siendo autoridad de Radar.
7. `updated_since` no comunica retiradas porque filtra eventos todavía públicos. Antes del corte hace falta un registro de cambios con retiradas explícitas y reconciliación, descrito en [el inventario de brechas](radar-api-central-gap.md).

## Mapeo mínimo

| Radar | Luna |
|---|---|
| `id` | `radar_event_id` |
| `title`, `summary`, `description` | contenido de la ficha consumida |
| `starts_at`, `ends_at`, `schedule`, `time_zone` | instantes, actividades y zona IANA del evento cuando está verificada |
| `event_status`, `attendance_mode` | estado y modalidad |
| `place`, `online_url` | ubicación pública |
| `organizer` | responsable público |
| `categories`, `audiences` | descubrimiento y preferencias |
| `admission_type`, `admission_options` | acceso y costos |
| `source_url`, `description_license`, `license_url` | procedencia y licencia pública cuando exista; `license_url` es `null` si sólo hay un permiso registrado |
| `schema_url`, `rdf_url`, `calendar_url` | interoperabilidad y exportación |
| `updated_at` | cursor de sincronización |

## Activación segura

La integración no se activa hasta que la API de Radar esté desplegada, tenga publicaciones reales aprobadas y pase pruebas de contrato, permisos, rendimiento y retirada. El cambio se hace detrás de una bandera en Luna: primero lectura paralela y comparación, después un grupo limitado y finalmente el corte. La bandera permite volver temporalmente al origen anterior durante la migración sin modificar ni borrar los datos canónicos de Radar.

Luna debe aplicar timeout, reintento con retroceso y caché de última respuesta válida. Un fallo de Radar no puede convertir borradores en contenido público ni provocar la eliminación masiva de eventos; las retiradas se confirman individualmente o mediante una ventana de reconciliación.
