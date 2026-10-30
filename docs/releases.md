# Releases

Radar Community utiliza Semantic Versioning:

- `v0.1.0`: landing “Próximamente”.
- `v0.1.1`: correcciones compatibles de la landing.
- `v0.2.0-alpha.1`: primera alpha funcional.
- `v0.2.0-beta.1`: beta posterior.
- `v1.0.0`: primera versión estable.

## Preparar una versión

1. Define el alcance y actualiza `CHANGELOG.md`.
2. Confirma la versión en `frontend/package.json`.
3. Ejecuta formato, lint, tipos, pruebas existentes y build.
4. Revisa accesibilidad y responsive en navegador.
5. Integra el cambio mediante pull request a `main`.
6. Espera a que CI y el deployment de producción estén correctos.
7. Verifica que el deployment use exactamente el commit de `main` que se etiquetará.
8. Crea el tag anotado sin mover o reemplazar tags anteriores.
9. Publica el GitHub Release con notas verificadas.

## Notas preparadas para v0.1.0

```markdown
# Radar Community v0.1.0

Primera versión pública de la presencia web de Radar Cultural.

## Added
- Landing "Próximamente".
- Diseño responsive.
- Identidad visual inicial.
- Configuración de Vue 3, Vite y TypeScript.
- Configuración inicial del repositorio y CI.
- Preparación para despliegue en Vercel.

## Notes
El sistema de gestión de eventos todavía se encuentra en desarrollo.
Esta versión no incluye la API ni el backend.
```

El tag será `v0.1.0` y el título `Radar Community v0.1.0 — Próximamente`. No se publicará hasta comprobar el deployment real.

