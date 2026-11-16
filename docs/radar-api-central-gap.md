# Radar como API central: brechas frente a Luna

Este documento separa las funciones comprobables en el código local de Radar Community de las
que faltan para que Luna y las próximas agendas consuman a Radar como motor principal. Es un
plan para convertir en issues y contratos; no describe funciones desplegadas.

## Decisión de autoridad

Radar Cultural será la fuente canónica de categorías, públicos, lugares, organizaciones, eventos,
horarios, licencias y estado editorial. También será la fuente principal de preferencias
culturales, favoritos, asistencia, recordatorios y notificaciones por persona. Luna y las futuras
agendas presentarán esas funciones como clientes. La personalización visual de tarjetas y los
datos académicos propios de Luna permanecen allí.

La lectura anónima del catálogo sigue siendo de sólo lectura. Las futuras operaciones privadas
requieren autenticación y autorización diferenciadas. No se copian cuentas, credenciales, tokens
OAuth, suscripciones push ni historiales personales desde Luna por traslado de base de datos.
Cualquier migración de personas necesita consentimiento, mapeo de identidad y procedimientos
de corrección y retirada.

## Estado actual

- **Radar local:** modelos UUID de usuarios, organizaciones, eventos, catálogos y moderación;
  publicación y revisión mediante Django Admin; API DRF pública paginada para eventos y
  catálogos; filtros, ficha HTML, Schema.org JSON-LD/RDF/XML e iCalendar. Vue consume esa API
  en desarrollo local.
- **Radar pendiente:** identidad compartida y autenticación de clientes externos; endpoints
  privados y modelos de preferencias, favoritos, asistencia, recordatorios y notificaciones;
  contribución por API; entrega programada; registro de retiradas para consumidores.
- **Producción:** el backend aún no está desplegado. Los tres eventos DEMO se generan sólo en
  SQLite con `DEBUG=True`; no son programación real ni datos para sincronizar con Luna.

## Inventario de paridad

| Capacidad existente en Luna | Radar hoy | Resultado necesario en Radar |
|---|---|---|
| Eventos, actividades, categorías, públicos, lugares, organizadores, licencias y Schema.org | Modelos, Admin y lectura pública | Operar con publicaciones reales aprobadas y pruebas de contrato. |
| Cuentas y perfil de gustos | Usuario UUID básico; sin cuenta pública ni preferencias | Identidad entre agendas, preferencias culturales privadas, consentimiento y gestión de cuenta. Los estilos de tarjeta quedan fuera. |
| Descubrimiento por intereses y exploración general | Búsqueda y filtros públicos; selección aleatoria limitada al hero | Descubrimiento paginado y estable con intereses optativos y exploración amplia, sin ordenar por métricas de interacción. |
| Eventos guardados (`EventBookmark`) | Sin modelo ni endpoint | Favoritos por persona y evento, lista paginada y alta/baja idempotente. |
| Asistencia (`EventAttendance`) | Sin modelo ni endpoint | Estado privado por persona y evento, transiciones válidas y reglas para eventos retirados o pasados. |
| Recordatorios (`EventReminder`, `ReminderDelivery`) | iCalendar sin estado personal | Preferencias, programación, entregas idempotentes y actualización por reprogramación/cancelación. |
| Notificaciones y lectura (`Notification`) | Sin modelo ni endpoint | Bandeja privada paginada, marcar como leída y política de retención. |
| Push y Google Calendar | Sin conexión ni entrega | Consentimiento, secretos protegidos, revocación y trabajos aislados antes de ofrecer esos canales. |
| Creación, colaboración y reportes | Gestión y moderación mediante Admin; sin API de contribución | Borradores autenticados, propiedad y permisos por objeto, revisión, reportes y auditoría. Evaluar invitaciones sin copiar mecánicas específicas de Luna. |
| Consumo desde otras agendas | `updated_since` sobre eventos todavía públicos | Cursor estable y registro de altas, cambios y retiradas; contrato de errores, cuotas y versión. |

El inventario no obliga a publicar todo en una versión. Push y Google Calendar tienen más
dependencias de privacidad y operación que el estado personal básico. Tickets, datos académicos
y presentación visual de Luna no son parte automática del motor cultural común.

## Orden de implementación y criterios de cierre

1. **Contrato e identidad.** Registrar en issue/ADR un sujeto de usuario estable, vínculo de
   cuentas de Luna, autenticación de navegador y servidor a servidor, alcance por cliente,
   revocación, consentimiento y política de datos. Diseñar la API privada en
   `backend/openapi.yaml` antes del código. Probar aislamiento entre personas y clientes.
2. **Estado personal esencial.** Crear preferencias, favoritos, asistencia y recordatorios con
   migraciones, unicidad, permisos por objeto, operaciones idempotentes y respuestas privadas
   sin caché compartida. Añadir bandeja y entrega de notificaciones con reintentos acotados y
   deduplicación. Probar CSRF con sesiones, abuso, borrado, corrección y revocación.
3. **Contribución cultural.** Permitir borradores autenticados y cambios revisados sin
   publicación directa. Conservar revisión editorial, atribución, licencias, reportes y retirada.
   Ninguna agenda obtiene permiso implícito para modificar eventos de terceros.
4. **Sincronización de consumidores.** `updated_since` sólo devuelve eventos todavía públicos;
   no informa que uno fue ocultado, retirado o perdió una organización verificada. Añadir
   registro/cursor de cambios con retiradas explícitas y reconciliación probada. Conservar el
   UUID como identidad estable; no sincronizar por slug, título ni URL.
5. **Canales y descubrimiento.** Añadir selección por intereses sin ranking basado en vistas,
   guardados o asistencia. Incorporar correo, push o calendario externo sólo tras definir
   consentimiento, seguridad de credenciales, trabajos, observabilidad y bajas.
6. **Operación y corte.** Completar aviso de privacidad y términos con datos legales reales;
   desplegar con PostgreSQL, respaldo y servicio dedicado; publicar eventos aprobados; verificar
   contrato, seguridad, rendimiento y retirada. Migrar Luna detrás de una bandera: lectura
   paralela, comparación, grupo limitado y corte gradual con rollback documentado.

Cada bloque debe convertirse en issues enfocadas. No se considera terminado por tener un
modelo, un test local o un build: exige pruebas de contrato, permisos, integración de cliente y,
para el corte, evidencia del dominio público.
