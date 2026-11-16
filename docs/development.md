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
Para ver la agenda y sus estados reales, inicia también el backend en otra terminal; sin ese proceso la interfaz muestra su estado de error de conexión. La base local vacía muestra el estado de agenda aún sin publicaciones.

Para revisar el recorrido completo con tres publicaciones **ficticias y marcadas DEMO**, usa la
SQLite local después de migrar, antes de iniciar ambos servidores:

```bash
cd backend
DEBUG=True .venv/bin/python manage.py seed_demo_events --frontend-origin http://127.0.0.1:5174
DEBUG=True .venv/bin/python manage.py runserver 127.0.0.1:8002

# En otra terminal:
cd frontend
API_PROXY_TARGET=http://127.0.0.1:8002 pnpm dev --host 127.0.0.1 --port 5174
```

Abre `http://127.0.0.1:5174/`: el hero enlaza a las tres fichas y `/agenda/` muestra la misma
respuesta de `/api/v1/events/`. El comando sólo funciona con `DEBUG=True` y SQLite, acepta
únicamente un origen local para las imágenes y puede repetirse sin duplicar eventos. Sus enlaces
`example.test`, títulos y horarios son datos de prueba; no los copies a producción ni a Luna.
El taller DEMO muestra un programa y un acceso de prueba en EUR en una sede ficticia de Francia;
la música DEMO usa `Asia/Tokyo` para comprobar las zonas horarias internacionales.
Si `8002` está ocupado en otra máquina, elige otro puerto libre y usa el mismo en
`API_PROXY_TARGET`.

## Backend

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --requirement requirements-dev.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

La configuración falla de forma explícita en producción si faltan `DJANGO_SECRET_KEY` o `DATABASE_URL`, si la base no es PostgreSQL o si `DJANGO_ALLOWED_HOSTS` contiene `*`. Nunca reutilices el secreto de desarrollo.

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

El flujo para cambios es contrato → pruebas → implementación. Los errores, paginación y permisos forman parte del contrato. Valida los artefactos locales antes de cerrar el cambio:

```bash
postman spec lint backend/openapi.yaml --fail-severity warning --no-report-events
postman collection lint "postman/collections/Radar Cultural API"
```

La ejecución conductual de la colección requiere un backend local y una base desechable preparada; consulta `docs/api.md`.
