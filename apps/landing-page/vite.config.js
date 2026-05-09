import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,        // Agar bisa diakses dari luar container
    port: 5173,        // Port internal
    strictPort: true,
    // Tambahkan ini agar tidak kena error "Invalid Host header"
    allowedHosts: [
      'aidetection.mektan.my.id',
      'localhost'
    ],
    watch: {
      usePolling: true,
    },
  },
})