# Arquitectura

## Alcance actual

La versión `v0.1.0` es una aplicación estática ubicada en `frontend/`. Vue compone la interfaz, Vite gestiona el entorno de desarrollo y genera `frontend/dist`, y TypeScript aporta validación estática.

```text
Navegador → frontend estático en Vercel
```

No existe una API, base de datos, autenticación ni servicio de eventos en esta etapa. La landing no simula solicitudes a servicios inexistentes.

## Evolución prevista

Cuando exista trabajo funcional real se agregará `backend/` con Python, Django, Django REST Framework y PostgreSQL. Ese backend tendrá un ciclo de despliegue independiente en infraestructura Linux propia con Nginx y Gunicorn.

```text
Navegador → frontend
                ↓ API futura
        Django REST Framework → PostgreSQL
```

La interfaz entre frontend y backend deberá documentarse antes de implementarse. Los datos de eventos se modelarán para facilitar su interoperabilidad con Schema.org, sin publicar datos estructurados de eventos que todavía no existan.

## Límites

- Vercel publica únicamente `frontend/`.
- La documentación y la configuración del repositorio no forman parte del artefacto web.
- Los secretos nunca se incorporan al bundle de Vite.
- Toda variable prefijada con `VITE_` es pública para el navegador y debe tratarse como tal.
- Radar Community y Radar Institutional comparten misión, pero no deben mezclar código o capacidades comerciales sin una decisión de arquitectura.

