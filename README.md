# Radar Community

Radar Cultural es una iniciativa mexicana que busca conectar a las personas con eventos, experiencias y espacios culturales. La plataforma pública estará orientada a la difusión cultural gratuita y al uso de datos abiertos, estructurados e interoperables, con una evolución prevista hacia Schema.org.

Este repositorio contiene **Radar Community**, la edición comunitaria y colaborativa de la plataforma. **Radar Institutional** será un producto comercial separado para organizaciones que necesiten agendas personalizadas, integraciones, analítica y administración avanzada.

## Estado del proyecto

`v0.1.0` prepara la primera presencia web de Radar Cultural: una landing estática de “Próximamente”. El sistema de gestión de eventos, la API y el backend todavía no forman parte de esta versión.

## Tecnologías

- Vue 3 con Composition API.
- Vite y TypeScript.
- pnpm.
- GitHub Actions para calidad y compilación.
- Vercel para publicar únicamente `frontend/`.

El backend futuro se construirá con Python, Django, Django REST Framework y PostgreSQL, y se desplegará en infraestructura Linux propia. No existe un backend dentro de este repositorio en la versión actual.

## Desarrollo local

### Requisitos

- Node.js 22.12 o posterior.
- pnpm 11 o posterior.

### Instalación

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

La aplicación estará disponible en la URL indicada por Vite, normalmente `http://localhost:5173`.

### Comandos

```bash
pnpm dev          # servidor local
pnpm lint         # análisis estático
pnpm typecheck    # comprobación de TypeScript y Vue
pnpm format:check # validación de formato
pnpm build        # validación de tipos y compilación a dist/
pnpm preview      # vista previa del build
```

## Estructura

```text
frontend/  Aplicación Vue y recursos públicos
docs/      Arquitectura, desarrollo, despliegue y releases
.github/   CI, Dependabot y plantillas de colaboración
```

`backend/` se incorporará cuando exista una implementación real. No se mantiene una carpeta vacía ni una API simulada.

## Contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir una propuesta. Los cambios se realizan en ramas de trabajo, pasan por pull request y usan títulos basados en Conventional Commits.

## Versiones

El proyecto sigue [Semantic Versioning](https://semver.org/) y mantiene sus cambios en [CHANGELOG.md](CHANGELOG.md). El flujo completo se documenta en [docs/releases.md](docs/releases.md).

## Licenciamiento

La licencia definitiva de Radar Community está en evaluación. El archivo [LICENSE](LICENSE) es un aviso provisional y **no concede automáticamente permisos de uso, modificación, distribución o explotación comercial**. Este proyecto no debe describirse todavía como software open source.

