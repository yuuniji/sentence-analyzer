<template>
  <div class="glass-panel input-panel">
    <h2>句子输入</h2>
    <textarea 
      v-model="store.inputSentence" 
      placeholder="请输入需要解析的英语长难句..."
      rows="5"
      :disabled="store.isStreaming"
    ></textarea>
    
    <div class="controls">
      <div class="options">
        <label>
          解析模式：
          <select v-model="store.selectedMode" :disabled="store.isStreaming">
            <option value="standard">标准解析</option>
            <option value="compact">精简模式</option>
            <option value="paragraph">段落模式</option>
          </select>
        </label>
        <label style="margin-left: 12px;">
          模型：
          <select v-model="store.selectedModel" :disabled="store.isStreaming">
            <option v-if="store.availableModels.length === 0" value="">加载中...</option>
            <option v-for="m in store.availableModels" :key="m.name" :value="m.name">
              {{ m.display_name }}
            </option>
          </select>
        </label>
      </div>
      <button 
        class="analyze-btn" 
        @click="store.analyze" 
        :disabled="!store.canAnalyze"
      >
        {{ store.isStreaming ? '正在解析...' : '开始解析 ✨' }}
      </button>
    </div>
    
    <div v-if="store.errorMessage" class="error-msg">
      {{ store.errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()

onMounted(() => {
  store.loadModels()
})
</script>

<style scoped>
.input-panel {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
h2 {
  font-size: 1.25rem;
  font-weight: 600;
}
textarea {
  width: 100%;
  background: rgba(0,0,0,0.2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 1rem;
  resize: vertical;
  transition: all 0.3s;
}
textarea:focus {
  outline: none;
  border-color: var(--accent-hover);
  background: rgba(0,0,0,0.3);
}
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.options select {
  background: rgba(0,0,0,0.3);
  color: white;
  border: 1px solid var(--border-color);
  padding: 8px 12px;
  border-radius: 6px;
  font-family: inherit;
}
.analyze-btn {
  background: var(--accent-color);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
}
.analyze-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-2px);
}
.analyze-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.error-msg {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}
</style>
