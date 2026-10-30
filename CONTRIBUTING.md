# Contribuir a Radar Community

Gracias por tu interés en Radar Cultural. En esta etapa aceptamos propuestas que mantengan el alcance de la landing y preparen una base clara para el trabajo comunitario posterior.

## Antes de comenzar

1. Revisa los issues existentes y evita duplicar propuestas.
2. Para cambios importantes, abre primero un feature request.
3. No publiques vulnerabilidades en un issue; sigue [SECURITY.md](SECURITY.md).
4. No incluyas secretos, datos personales, contenido sin autorización ni dependencias innecesarias.

## Flujo de trabajo

1. Crea una rama corta desde `main`, por ejemplo `feat/nueva-seccion`.
2. Instala las dependencias dentro de `frontend/` con `pnpm install --frozen-lockfile`.
3. Realiza cambios pequeños y enfocados.
4. Ejecuta `pnpm format:check`, `pnpm lint`, `pnpm typecheck` y `pnpm build`.
5. Abre un pull request usando la plantilla del repositorio.

Los títulos de pull requests y commits principales siguen esta convención:

- `feat:` funcionalidad nueva.
- `fix:` corrección de un defecto.
- `docs:` documentación.
- `chore:` mantenimiento.
- `refactor:` cambio interno sin alterar el comportamiento.
- `test:` pruebas.
- `ci:` integración continua.

## Interfaz y accesibilidad

- Conserva HTML semántico, contraste suficiente y navegación por teclado.
- Respeta `prefers-reduced-motion`.
- Comprueba como mínimo un viewport móvil y uno de escritorio.
- Adjunta capturas cuando el cambio sea visual.
- No agregues formularios, APIs o estados que simulen servicios inexistentes.

## Revisión

La revisión técnica cubre `frontend/`, workflows y configuración del repositorio. Cuando el equipo de GitHub `desarrollo-tecnico` esté activo y tenga acceso, se utilizará como propietario de estas rutas.

Al contribuir aceptas cumplir el [Código de Conducta](CODE_OF_CONDUCT.md). La aceptación de una contribución no modifica el estado provisional de la licencia.

