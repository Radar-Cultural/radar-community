# Releases

Radar Community utiliza Semantic Versioning:

- `v0.1.x`: presencia pública inicial.
- `v0.2.0-alpha.x`: primeras versiones de landing y API funcional.
- `v0.2.0-beta.x`: validación comunitaria y de datos.
- `v1.0.0`: primera versión estable.

## Preparar una versión

1. Define el alcance mediante milestone e issues.
2. Actualiza `CHANGELOG.md` y las versiones de artefactos.
3. Ejecuta los checks de frontend y backend.
4. Revisa migraciones y contrato OpenAPI.
5. Valida landing en escritorio, tableta y móvil.
6. Integra por PR con CI y CODEOWNERS.
7. Despliega el commit de `main` autorizado y verifica dominio, API y servicios por separado.
8. Etiqueta exactamente el commit desplegado.
9. Publica notas con cambios y limitaciones reales.

No reescribas tags ni uses un release de GitHub como prueba de producción. Un rollback se registra como operación y, si cambia código, produce una nueva versión.
