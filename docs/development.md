# Desarrollo

## Requisitos

- Node.js 22 o posterior y pnpm 11.
- Python 3.11–3.14.
- PostgreSQL para pruebas de integración previas al despliegue; SQLite basta para el ciclo local inicial.

## Frontend

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

El servidor queda normalmente en `http://127.0.0.1:5173`. `API_PROXY_TARGET` permite cambiar el backend local sin exponer la variable al bundle.

## Backend

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --requirement requirements-dev.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

La configuración falla de forma explícita en producción si faltan `DJANGO_SECRET_KEY` o `DATABASE_URL`. Nunca reutilices el secreto de desarrollo.

## Calidad

```bash
cd frontend
pnpm format:check && pnpm lint && pnpm typecheck && pnpm build

cd ../backend
.venv/bin/ruff format --check .
.venv/bin/ruff check .
DEBUG=True .venv/bin/python manage.py check
DEBUG=True .venv/bin/python manage.py makemigrations --check --dry-run
DEBUG=True .venv/bin/python manage.py test
```

## Modelos y migraciones

1. Modifica el modelo y sus pruebas.
2. Ejecuta `manage.py makemigrations <app>`.
3. Lee la migración; no la aceptes sólo porque fue generada.
4. Prueba desde cero y con datos heredados cuando altere unicidad, nulabilidad o índices.
5. No uses `--fake`, borres filas ni elimines índices sin diagnóstico del esquema real.

## API

El flujo para cambios es contrato → pruebas → implementación. Los errores, paginación y permisos forman parte del contrato. Ejecuta `postman status` al terminar trabajo de API cuando exista la colección local.
