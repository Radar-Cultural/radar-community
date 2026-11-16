import { defineConfig, loadEnv } from 'vite'
import { resolve } from 'node:path'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],
    server: {
      proxy: {
        '/api': {
          target: env.API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: false,
        },
        '/eventos/': {
          target: env.API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: false,
        },
        '/backend-static/': {
          target: env.API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: false,
        },
        '/sitemap-': {
          target: env.API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: false,
        },
        '/sitemap.xml': {
          target: env.API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: false,
        },
      },
    },
    build: {
      target: 'es2022',
      rollupOptions: {
        input: {
          home: resolve(process.cwd(), 'index.html'),
          agenda: resolve(process.cwd(), 'agenda/index.html'),
          privacidad: resolve(process.cwd(), 'privacidad/index.html'),
          terminos: resolve(process.cwd(), 'terminos/index.html'),
          conducta: resolve(process.cwd(), 'codigo-de-conducta/index.html'),
        },
      },
    },
  }
})
