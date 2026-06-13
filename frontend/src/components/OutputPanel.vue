<template>
  <div class="glass-panel output-panel" v-if="store.hasOutput">
    <div class="header">
      <h2>解析结果</h2>
      <div class="header-right">
        <div class="status-indicator" v-if="store.isStreaming">
          <span class="dot pulse"></span> 正在生成中...
        </div>
        <button class="copy-btn" v-else @click="copyMarkdown" :class="{ 'copied': copied }">
          <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          {{ copied ? '已复制格式' : '一键复制 Markdown' }}
        </button>
      </div>
    </div>
    
    <div class="output-content">
      <TabsRenderer :content="store.outputMarkdown" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'
import TabsRenderer from './TabsRenderer.vue'

const store = useAnalyzerStore()
const copied = ref(false)

function copyMarkdown() {
  if (!store.outputMarkdown) return
  navigator.clipboard.writeText(store.outputMarkdown).then(() => {
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  }).catch(err => {
    console.error('Copy failed', err)
  })
}
</script>

<style scoped>
.output-panel {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 300px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
h2 {
  font-size: 1.25rem;
  font-weight: 600;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--accent-hover);
  font-size: 0.9rem;
}
.copy-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 6px 12px;
  border-radius: 8px;

  font-size: 0.9rem;
}
.copy-btn:hover {
  background: var(--border-light);
  color: var(--text-primary);
}
.copy-btn.copied {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.3);
}
.dot {
  width: 8px;
  height: 8px;
  background-color: var(--accent-hover);
  border-radius: 50%;
}
.pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
.output-content {
  flex-grow: 1;
}
</style>
