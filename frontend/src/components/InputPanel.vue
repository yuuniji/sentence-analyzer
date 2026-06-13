<template>
  <div class="glass-panel input-panel">
    <!-- 篇章导读模式输入区 -->
    <div v-if="store.activeEngine === 'article'" class="input-wrapper animate-fade-in">
      <textarea 
        v-model="store.inputArticle" 
        placeholder="在此粘贴整篇外刊文章或文学章节，让 AI 为你进行宏观的主旨提炼、文风分析并扫出潜伏的长难句..."
        rows="8"
        :disabled="store.isStreaming"
      ></textarea>
    </div>

    <!-- 长难句精读模式输入区 -->
    <template v-else>
      <div class="input-wrapper animate-fade-in">
        <textarea 
          v-model="store.inputSentence" 
          placeholder="请输入需要解析的英语长难句..."
          rows="4"
          :disabled="store.isStreaming"
          class="main-textarea"
        ></textarea>
        <div class="hint-container">
          <div class="hint-text">
            💡 提示：保留原文排版可提升解析精度，例如 <code>*斜体*</code> 或 <code>**加粗**</code>
          </div>
          <button class="toggle-advanced-btn" @click="showAdvanced = !showAdvanced">
            {{ showAdvanced ? '隐藏高级选项' : '添加上下文 / 术语表' }}
          </button>
        </div>
      </div>

      <div v-if="showAdvanced" class="advanced-options animate-fade-in">
        <div class="advanced-field">
          <label>全景上下文</label>
          <textarea 
            v-model="store.inputContext" 
            placeholder="粘贴原著的整个段落或前后文，帮助大模型理解代词指代和语境..."
            rows="2"
            :disabled="store.isStreaming"
          ></textarea>
        </div>
        <div class="advanced-field">
          <label>专属术语表</label>
          <textarea 
            v-model="store.inputTerms" 
            placeholder="按 单词 = 译名 的格式输入，例如：The Force = 原力"
            rows="2"
            :disabled="store.isStreaming"
          ></textarea>
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
import { ref, onMounted, watch } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()
const showAdvanced = ref(false)

// 监测上下文和术语表，若有内容（如从历史记录载入），则自动展开高级选项面板
watch(
  [() => store.inputContext, () => store.inputTerms],
  ([newCtx, newTerms]) => {
    if ((newCtx && newCtx.trim()) || (newTerms && newTerms.trim())) {
      showAdvanced.value = true
    }
  },
  { immediate: true }
)

onMounted(() => {
  store.loadModels()
})
</script>

<style scoped>
.input-panel {
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Textareas */
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
textarea {
  width: 100%;
  background: var(--color-canvas);
  border: 1px solid var(--color-sage);
  border-radius: 12px;
  padding: 16px;
  color: var(--color-ink);
  font-size: 15px;
  font-family: var(--font-ui);
  resize: vertical;
  transition: border-color 0.2s, box-shadow 0.2s;
}
textarea:focus {
  outline: none;
  border-color: var(--color-hudson-blue);
  box-shadow: 0 0 0 1px var(--color-hudson-blue);
}
.main-textarea {
  font-size: 1.05rem;
}

/* Hints & Advanced toggle */
.hint-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 4px;
}
.hint-text {
  font-size: 13px;
  color: var(--color-steel);
}
.hint-text code {
  background: var(--color-canvas);
  border: 1px solid var(--color-sage);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: var(--color-ink);
}
.toggle-advanced-btn {
  background: transparent;
  border: none;
  color: var(--color-steel);
  font-size: 13px;
  font-weight: 500;
  transition: color 0.2s;
}
.toggle-advanced-btn:hover {
  color: var(--color-ink);
}

/* Advanced Options */
.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: var(--color-canvas);
  border: 1px dashed var(--color-sage);
  border-radius: 12px;
}
.advanced-field label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-steel);
  margin-bottom: 6px;
}
.advanced-field textarea {
  padding: 12px;
  font-size: 15px;
}

/* Controls */
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}
.options select {
  background: var(--color-canvas);
  color: var(--color-ink);
  border: 1px solid var(--color-sage);
  padding: 8px 12px;
  border-radius: 8px;
  font-family: inherit;
  font-size: 15px;
}
.options select:focus {
  outline: none;
  border-color: var(--color-steel);
}

/* CTA Pill Button */
.analyze-btn {
  padding: 10px 24px;
  background: var(--color-surface-nav); /* Dark fill */
  color: #ffffff;
  border: none;
  border-radius: var(--radius-btn);
  font-weight: 500;
  font-size: 15px;
  transition: all 0.2s;
}
.analyze-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: var(--shadow-nav);
}
.analyze-btn:disabled {
  background: var(--color-sage);
  color: var(--color-steel);
  cursor: not-allowed;
}

/* Error */
.error-msg {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  font-size: 0.9rem;
}
</style>
