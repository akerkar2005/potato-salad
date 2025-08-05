import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/potato-salad/',
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Bind to a specific IP or use '0.0.0.0' to listen on all interfaces
    port: 5173               // Optional: set your preferred port
  }
})

