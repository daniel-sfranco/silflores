import { defineConfig } from 'vite';

export default defineConfig({
  root: 'silfloresapp/static',
  base: '/static/',
  build: {
    manifest: true,
    outDir: 'silfloresapp/static/dist',
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    cors: {
      origin: 'http://localhost:8000',
      methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
      credentials: true,
    },
  },
});