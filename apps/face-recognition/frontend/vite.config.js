import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/face/',
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    // Tambahkan bagian ini untuk mengizinkan domain kamu
    allowedHosts: [
      'aidetection.mektan.my.id'
    ],
    // Opsional: Jika masih ada masalah dengan websocket (HMR)
    hmr: {
        clientPort: 443 
    }
  }
})