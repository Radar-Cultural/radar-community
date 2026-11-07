# Despliegue

## Estado real

La producción actual publica únicamente el frontend:

```text
Cloudflare Tunnel dedicado → Nginx 127.0.0.1:8093 → /var/www/radarcultural.mx/current
```

`current` es un enlace simbólico a un directorio inmutable bajo `releases/<commit>`. Cambiar el enlace hace atómica la publicación del frontend. El backend todavía no está desplegado y no existe un servicio Gunicorn de Radar Community.

## Actualizar el checkout

En el servidor, dentro del checkout de Radar Community:

```bash
git status --short
git fetch origin main
git merge --ff-only origin/main
```

El árbol debe estar limpio antes de actualizar. Si `git status` muestra cambios, detén el despliegue e identifica su propietario. No uses `git reset --hard`, `git clean -fd` ni sobrescribas trabajo del servidor.

`git merge --ff-only origin/main` y `git pull --ff-only origin main` son equivalentes para este flujo; se prefiere separar `fetch` y `merge` para poder inspeccionar el commit antes de aplicarlo.

## Publicar el frontend

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm format:check
pnpm lint
pnpm typecheck
pnpm build
cd ..

release_sha="$(git rev-parse --short=12 HEAD)"
release_dir="/var/www/radarcultural.mx/releases/$release_sha"
sudo install -d -o wac -g www-data -m 0750 "$release_dir"
sudo rsync -a --delete frontend/dist/ "$release_dir/"
sudo ln -sfn "$release_dir" /var/www/radarcultural.mx/current
```

Después verifica el origen y el dominio público. Una actualización de archivos no requiere reiniciar Nginx ni Cloudflared:

```bash
curl -fsSI -H 'Host: radarcultural.mx' http://127.0.0.1:8093/
curl -fsSI https://radarcultural.mx/
curl -fsS https://radarcultural.mx/robots.txt
```

Conserva al menos el release anterior. Para rollback del frontend, cambia `current` al release verificado anterior y repite las comprobaciones.

## Preparar el backend por primera vez

No ejecutes esta sección hasta contar con autorización, PostgreSQL, respaldo, variables y unidad systemd específica.

1. Crear `backend/.venv` con el Python de producción.
2. Instalar `backend/requirements.txt` dentro de esa venv.
3. Crear base y usuario PostgreSQL con privilegios sólo sobre su propia base.
4. Guardar variables en un archivo root-only fuera del repositorio.
5. Ejecutar `check --deploy`, migraciones y `collectstatic`.
6. Crear `radar-community-api.service` con Gunicorn y un socket dedicado.
7. Añadir en el sitio Nginx únicamente `/api/`, `/admin/` y `/backend-static/` hacia ese socket.
8. Mantener el mismo túnel: Cloudflare sigue apuntando a Nginx `8093`.
9. Verificar `GET /api/v1/status/`, un catálogo vacío y que `POST /api/v1/events/` responda `405`.

## Actualizar frontend y backend

Cuando el backend esté operativo:

```bash
git fetch origin main
git merge --ff-only origin/main

backend/.venv/bin/python -m pip install --requirement backend/requirements.txt
backend/.venv/bin/python backend/manage.py check
backend/.venv/bin/python backend/manage.py migrate --noinput
backend/.venv/bin/python backend/manage.py collectstatic --noinput
sudo systemctl restart radar-community-api.service
sudo systemctl is-active radar-community-api.service
curl -fsS https://radarcultural.mx/api/v1/status/
```

Publica el frontend con un nuevo directorio de release después de que la API requerida esté sana. No reinicies servicios ajenos ni la instancia general de Cloudflared.

## Rollback del backend

Un rollback de código no revierte automáticamente el esquema. Antes de una migración de producción, confirma respaldo y reversibilidad. Si el cambio es incompatible, aplica el procedimiento documentado para esa migración; no uses `migrate --fake` como atajo.
