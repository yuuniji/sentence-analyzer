<template>
  <div class="glass-panel history-panel">
    <h3>历史记录</h3>
    
    <div class="history-list" v-if="store.history.length > 0">
      <div 
        v-for="record in store.history" 
        :key="record.id" 
        class="history-item"
        :class="{ active: store.currentRecordId === record.id }"
        @click="store.loadRecord(record)"
      >
        <div class="record-sentence">{{ truncate(record.sentence) }}</div>
        <div class="record-meta">
          <span class="mode-tag">{{ record.mode }}</span>
          <div class="meta-right">
            <span class="time">{{ formatDate(record.created_at) }}</span>
            <button class="delete-btn" @click.stop="store.deleteRecord(record.id)" title="删除记录">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      暂无历史记录
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()

onMounted(() => {
  store.loadHistory()
})

function truncate(str, len = 40) {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  // 考虑到 UTC 时区转本地时间
  const d = new Date(dateStr + 'Z')
  return `${d.getMonth() + 1}-${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
}
</script>

<style scoped>
.history-panel {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
h3 {
  font-size: 1.1rem;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}
.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  flex-grow: 1;
  padding-right: 4px;
}
.history-item {
  padding: 12px;
  border-radius: 8px;
  background: rgba(255,255,255,0.03);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}
.history-item:hover {
  background: rgba(255,255,255,0.06);
  border-color: var(--border-color);
}
.history-item.active {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}
.record-sentence {
  font-size: 0.95rem;
  margin-bottom: 8px;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.record-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--text-secondary);
}
.meta-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.delete-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.2s;
}
.history-item:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}
.mode-tag {
  background: rgba(0,0,0,0.3);
  padding: 2px 6px;
  border-radius: 4px;
}
.empty-state {
  color: var(--text-secondary);
  text-align: center;
  margin-top: 40px;
  font-size: 0.95rem;
}
</style>
