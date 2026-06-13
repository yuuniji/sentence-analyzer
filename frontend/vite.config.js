import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174, // 使用 5174 端口，避免与之前运行过的 VitePress 项目（默认 5173）产生浏览器缓存冲突
    strictPort: false
  }
})
