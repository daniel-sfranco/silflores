import { defineConfig } from 'vite';

export default defineConfig({
  root: 'silfloresapp/static',
  base: '/static/',
  build: {
    manifest: true,
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: 'src/js/main.js',
        home_carousel: 'src/js/home_carousel.js',
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    cors: true,
  },
});