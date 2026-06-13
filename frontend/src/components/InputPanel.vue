<template>
  <div class="glass-panel input-panel">
    <div class="engine-tabs">
      <button 
        :class="['engine-tab', { active: store.activeEngine === 'sentence' }]"
        @click="store.activeEngine = 'sentence'"
      >长难句精读</button>
      <button 
        :class="['engine-tab', { active: store.activeEngine === 'article' }]"
        @click="store.activeEngine = 'article'"
      >篇章导读</button>
    </div>

    <!-- 篇章导读模式输入区 -->
    <div v-if="store.activeEngine === 'article'" class="input-wrapper animate-fade-in">
      <textarea 
        v-model="store.inputArticle" 
        placeholder="在此粘贴整篇外刊文章或文学章节，让 AI 为你进行宏观的主旨提炼、文风分析并扫出潜伏的长难句..."
        rows="10"
        :disabled="store.isStreaming"
      ></textarea>
    </div>

    <!-- 长难句精读模式输入区 -->
    <template v-else>
      <details class="context-details">
      <summary>添加上下文语境 (全景精读模式)</summary>
      <textarea 
        v-model="store.inputContext" 
        placeholder="在此粘贴原著的整个段落或前后文，帮助大模型理解代词指代和特殊排版含义..."
        rows="3"
        class="context-input"
        :disabled="store.isStreaming"
      ></textarea>
    </details>

    <details class="context-details">
      <summary>自定义术语表 (专有名词/自创词解析)</summary>
      <textarea 
        v-model="store.inputTerms" 
        placeholder="按 单词 = 译名 的格式输入，例如：&#10;The Force = 原力&#10;Muggle = 麻瓜"
        rows="2"
        class="context-input"
        :disabled="store.isStreaming"
      ></textarea>
    </details>

    <div class="input-wrapper">
      <textarea 
        v-model="store.inputSentence" 
        placeholder="请输入需要解析的英语长难句..."
        rows="4"
        :disabled="store.isStreaming"
      ></textarea>
      <div class="hint-text">
        💡 提示：保留书籍原文排版可提升解析精度，例如使用 <code>*斜体*</code> 或 <code>**加粗**</code>
      </div>
    </div>
    </template>
    
    <div class="controls">
      <div class="options">
        <label v-if="store.activeEngine === 'sentence'">
          解析模式：
          <select v-model="store.selectedMode" :disabled="store.isStreaming">
            <option value="standard">标准解析</option>
            <option value="compact">精简模式</option>
            <option value="paragraph">段落模式</option>
          </select>
        </label>
        <label :style="{ marginLeft: store.activeEngine === 'sentence' ? '12px' : '0' }">
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
.engine-tabs {
  display: flex;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 99px; /* Pill shape */
  padding: 4px;
  margin-bottom: 8px;
}
.engine-tab {
  flex: 1;
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 99px;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}
.engine-tab:hover {
  color: var(--text-primary);
}
.engine-tab.active {
  background: var(--border-color);
  color: var(--text-primary);
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.input-panel {
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
textarea {
  width: 100%;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  color: var(--text-primary);
  font-size: 1.05rem;
  font-family: var(--font-sans);
  resize: vertical;
  transition: border-color 0.2s;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}
textarea:focus {
  outline: none;
  border-color: rgba(255,255,255,0.2);
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
  padding: 10px 24px;
  background: var(--text-primary);
  color: var(--bg-color);
  border: none;
  border-radius: 99px;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.2s;
}
.analyze-btn:hover:not(:disabled) {
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255,255,255,0.15);
}
.analyze-btn:disabled {
  background: var(--border-color);
  color: var(--text-muted);
  cursor: not-allowed;
}
.error-msg {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.context-details {
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0;
}
.context-details summary {
  padding: 12px 16px;
  font-size: 0.95rem;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.context-details summary::after {
  content: "▾";
  transition: transform 0.2s;
}
.context-details[open] summary::after {
  transform: rotate(180deg);
}
.context-details[open] summary {
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
}
.context-input {
  border: none;
  border-radius: 0 0 8px 8px;
  background: transparent;
  padding: 16px;
  font-size: 0.95rem;
  color: var(--text-secondary);
}
.context-input:focus {
  background: rgba(0,0,0,0.1);
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.hint-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  padding-left: 4px;
}
.hint-text code {
  background: rgba(255,255,255,0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: var(--accent-hover);
}
</style>
