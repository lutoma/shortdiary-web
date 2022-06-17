import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  // Only used during development, in production proxying is done by caddy
  server: {
    proxy: {
      '/map/': {
        target: 'https://api.mapbox.com',
        rewrite: (path) => path.replace(/^\/map/, '')
      },
      '/avatar/': 'https://www.gravatar.com/',
      '/geocode/': 'https://api.opencagedata.com'
    },
  }
})
