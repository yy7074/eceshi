import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import path from 'node:path'

const inputDir = process.cwd()
process.env.UNI_INPUT_DIR = process.env.UNI_INPUT_DIR || inputDir
process.env.UNI_CLI_CONTEXT = process.env.UNI_CLI_CONTEXT || inputDir
process.env.VITE_ROOT_DIR = process.env.VITE_ROOT_DIR || inputDir
process.env.UNI_PLATFORM = process.env.UNI_PLATFORM || 'h5'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni.default ? uni.default({ viteLegacyOptions: false }) : uni({ viteLegacyOptions: false })
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
