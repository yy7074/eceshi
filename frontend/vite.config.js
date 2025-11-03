import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni.default ? uni.default() : uni()
  ],
  base: '/h5/',
  server: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'https://catdog.dachaonet.com',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: 'dist/h5',
    assetsDir: 'static',
    sourcemap: false,
    minify: 'terser',
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vuex'],
          'uni-vendor': ['@dcloudio/uni-h5']
        }
      }
    }
  },
  optimizeDeps: {
    exclude: ['vue-demi']
  }
})

