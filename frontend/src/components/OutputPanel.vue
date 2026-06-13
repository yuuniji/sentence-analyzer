<template>
  <div class="glass-panel output-panel" v-if="store.hasOutput">
    <div class="header">
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
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.header {
  display: flex;
  justify-content: flex-end;
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
  color: var(--color-hudson-blue);
  font-size: 15px;
}
.copy-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 1px solid var(--color-slate-cyan);
  color: var(--color-slate-cyan);
  padding: 6px 12px;
  border-radius: var(--radius-btn);
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
}
.copy-btn:hover {
  background: var(--color-slate-cyan);
  color: #ffffff;
}
.copy-btn.copied {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.3);
}
.dot {
  width: 8px;
  height: 8px;
  background-color: var(--color-hudson-blue);
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
