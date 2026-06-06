import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/', // Replace with your backend server URL
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), //removing "/api" prefix if the server doesnt expect it!
      },
    },
  } 
})


