# Radar Community

Radar Cultural es una iniciativa mexicana para descubrir, compartir y preservar la vida cultural mediante difusión gratuita, datos abiertos y tecnología responsable.

Este repositorio contiene **Radar Community**, la edición colaborativa. **Radar Institutional** es un producto separado para organizaciones con necesidades comerciales de agendas, integraciones y analítica.

## Estado

- `v0.1.0`: landing “Próximamente”, publicada.
- `v0.2.0` en desarrollo: nueva identidad de la landing y primera API de lectura pública.
- La API y el backend todavía no están desplegados en producción.

No se mantienen eventos ficticios, fechas de lanzamiento, cifras, alianzas ni formularios simulados.

## Stack

- Frontend: Vue 3, Vite, TypeScript y pnpm.
- Backend: Python, Django 5.2, Django REST Framework y PostgreSQL.
- Producción actual: Nginx y Cloudflare Tunnel; Gunicorn se incorporará cuando se autorice el backend.
- Calidad: GitHub Actions, Ruff, ESLint, Vue TypeScript y pruebas de Django.

## Desarrollo rápido

Frontend:

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

Backend:

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --requirement requirements-dev.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Vite envía `/api` a `http://127.0.0.1:8000` durante el desarrollo, de forma que no se necesita CORS abierto.

## Estructura

```text
frontend/          Landing y futura aplicación Vue
backend/           Django, DRF, modelos, migraciones y OpenAPI
postman/           Colección local generada desde el contrato y sus aserciones
docs/              Arquitectura, desarrollo, API y despliegue
.github/           CI, plantillas y automatización de dependencias
AGENTS.md          Contexto seguro para contribuciones asistidas por IA
```

## Documentación

- [Arquitectura](docs/architecture.md)
- [Backend y seguridad](docs/backend.md)
- [Contrato de API](docs/api.md)
- [Desarrollo](docs/development.md)
- [Despliegue](docs/deployment.md)
- [Sistema visual](docs/design-system.md)
- [Trabajo pendiente](docs/roadmap.md)
- [Contribuir](CONTRIBUTING.md)
- [Seguridad](SECURITY.md)

## Licencia

La licencia definitiva de Radar Community continúa en evaluación. El archivo [LICENSE](LICENSE) es un aviso provisional y no concede automáticamente permisos de uso, modificación, distribución o explotación comercial. El proyecto no debe presentarse todavía como open source aprobado.
