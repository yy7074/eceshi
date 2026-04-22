import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import path from 'node:path'

const inputDir = process.cwd()
process.env.UNI_INPUT_DIR = process.env.UNI_INPUT_DIR || inputDir
process.env.UNI_CLI_CONTEXT = process.env.UNI_CLI_CONTEXT || inputDir
process.env.VITE_ROOT_DIR = process.env.VITE_ROOT_DIR || inputDir
process.env.UNI_PLATFORM = process.env.UNI_PLATFORM || 'h5'
const platform = process.env.UNI_PLATFORM
const isH5 = platform === 'h5'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    uni.default ? uni.default({ viteLegacyOptions: false }) : uni({ viteLegacyOptions: false })
  ],
  base: isH5 ? '/web/' : './',
  server: isH5
    ? {
        port: 8080,
        host: '0.0.0.0',
        proxy: {
          '/api': {
            target: 'https://catdog.dachaonet.com',
            changeOrigin: true,
            secure: false
          }
        }
      }
    : undefined,
  build: {
    outDir: path.join('dist', mode === 'development' ? 'dev' : 'build', platform),
    assetsDir: 'static',
    sourcemap: false,
    minify: 'terser',
    chunkSizeWarningLimit: 1500,
    rollupOptions: isH5
      ? {
          output: {
            manualChunks: {
              'vue-vendor': ['vue', 'vuex'],
              'uni-vendor': ['@dcloudio/uni-h5']
            }
          }
        }
      : undefined
  },
  optimizeDeps: {
    exclude: ['vue-demi']
  }
}))
