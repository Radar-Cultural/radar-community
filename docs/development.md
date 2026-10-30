# Desarrollo

## Preparación

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

La versión de Node y pnpm debe respetar `frontend/package.json`. No uses `npm install` ni regeneres el lockfile con otro gestor.

## Calidad local

Antes de abrir un pull request:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm build
test -f dist/index.html
```

Si se incorporan pruebas, el script `test` debe ejecutarlas de forma no interactiva y CI lo ejecutará automáticamente.

## Convenciones

- Composition API con `<script setup lang="ts">`.
- Componentes pequeños y semánticos dentro de `src/components/`.
- Tokens visuales globales en `src/styles/`.
- Recursos procesados por Vite dentro de `src/assets/`.
- Recursos públicos sin transformación dentro de `public/`.
- Cero secretos y cero rutas personales en el repositorio.

## Accesibilidad y responsive

- La navegación completa debe funcionar con teclado.
- Todo contenido gráfico necesita alternativa textual apropiada.
- El movimiento debe desactivarse con `prefers-reduced-motion`.
- Comprueba como mínimo 1440×900, 768×1024 y 390×844.
- Revisa que no existan desbordamientos, texto cortado ni pérdida de contraste.

