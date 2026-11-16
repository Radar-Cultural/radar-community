# Contribuir a Radar Community

Gracias por colaborar con Radar Cultural. Antes de escribir código, revisa el alcance, las issues abiertas y la política de seguridad.

## Antes de comenzar

1. Busca una issue existente. Para cambios funcionales, abre o solicita una antes del PR.
2. Usa el formulario adecuado y selecciona el área afectada.
3. Para API o modelos, describe permisos, compatibilidad, migración y datos expuestos.
4. No publiques vulnerabilidades: utiliza [Security Advisories](https://github.com/Radar-Cultural/radar-community/security/advisories/new).
5. No incluyas secretos, datos personales, eventos ficticios ni contenido sin fuente y autorización.

## Ramas, commits y PR

- Crea una rama corta desde `main` con prefijo `feature/`, `fix/`, `update/`, `docs/`, `test/`, `ci/` o `refactor/`; por ejemplo, `feature/radar-community-alpha` o `fix/mobile-header`. `update/` se reserva para contenido o dependencias sin cambio funcional.
- Mantén un cambio enfocado por PR.
- Usa títulos de PR `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:` o `ci:`. Los dos puntos pertenecen al título; en la rama se usa `/`. Un trabajo `update/` usa `chore:` o `docs:` según su contenido.
- Vincula la issue con `Closes #...`.
- Adjunta capturas de escritorio y móvil para cambios visuales.
- El merge preferido es squash después de CI y revisión de CODEOWNERS.

## Frontend

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm format:check
pnpm lint
pnpm typecheck
pnpm build
```

Comprueba teclado, foco, contraste, zoom, movimiento reducido y viewports de 1440×900, 768×1024 y 390×844. Conserva la identidad descrita en `docs/design-system.md`.

## Backend

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --requirement requirements-dev.txt
.venv/bin/ruff format --check .
.venv/bin/ruff check .
DEBUG=True .venv/bin/python manage.py check
DEBUG=True .venv/bin/python manage.py makemigrations --check --dry-run
DEBUG=True .venv/bin/python manage.py test
```

Cambios de API modifican primero `backend/openapi.yaml`. Cambios de modelos incluyen una migración revisada. No abras operaciones de escritura ni relajes permisos, CSRF, CORS o filtros de publicación sin una decisión documentada.

## Asistencia con IA

Lee `AGENTS.md` antes de usar una herramienta de IA. En el PR indica qué partes se generaron o revisaron con asistencia, qué verificaste manualmente y qué permanece sin validar. La persona autora sigue siendo responsable del cambio.

Al contribuir aceptas el [Código de Conducta](CODE_OF_CONDUCT.md). La aceptación de una contribución no modifica el estado provisional de la licencia.
