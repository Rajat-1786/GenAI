import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Forward API calls to the FastAPI backend so the browser stays same-origin (no CORS needed).
    proxy: {
      '/auth': 'http://localhost:8000',
    },
  },
})
