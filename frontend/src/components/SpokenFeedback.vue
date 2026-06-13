<template>
  <div class="spoken-feedback animate-fade-in" v-if="spokenResult">
    <div class="section-card corrections-card">
      <h3 class="section-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="title-icon"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="m9 12 2 2 4-4"></path></svg>
        口语纠错建议 (Corrections)
      </h3>
      
      <div class="text-display">
        <span 
          v-for="(segment, idx) in spokenResult.segments" 
          :key="idx" 
          class="word-wrapper"
        >
          <!-- correct -->
          <span v-if="segment.status === 'correct'" class="word-normal">{{ segment.text }}</span>
          
          <!-- deleted -->
          <span v-else-if="segment.status === 'deleted'" class="word-deleted strikethrough" title="多余，建议删除">{{ segment.text }}</span>
          
          <!-- filler -->
          <span v-else-if="segment.status === 'filler'" class="word-filler" title="语气停顿词">{{ segment.text }}</span>
          
          <!-- pause -->
          <span v-else-if="segment.status === 'pause'" class="word-pause" title="长停顿">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="color: var(--color-slate-cyan); flex-shrink: 0; display: inline-block; vertical-align: middle;"><rect x="14" y="4" width="4" height="16" rx="1"></rect><rect x="6" y="4" width="4" height="16" rx="1"></rect></svg>
          </span>
          
          <!-- indistinct -->
          <span v-else-if="segment.status === 'indistinct'" class="word-indistinct" title="含糊不清">{{ segment.text || '[含糊不清]' }}</span>
          
          <!-- insertion -->
          <span v-else-if="segment.status === 'insertion'" class="word-insertion" title="建议在此插入词汇">{{ segment.text }}</span>
          
          <!-- errors (pronunciation, grammar, vocabulary) -->
          <span v-else class="error-wrapper">
            <span :class="['word-error', `bg-${segment.status}`]" :title="getErrorTitle(segment.status)">
              {{ segment.text }}
            </span>
            <span v-if="segment.correction" class="word-correction" title="建议修正为">
              {{ segment.correction }}
            </span>
          </span>
        </span>
      </div>

      <!-- Legend Panel -->
      <div class="legend-panel">
        <div class="legend-item"><span class="legend-dot bg-pron"></span>发音错误</div>
        <div class="legend-item"><span class="legend-dot bg-vocab"></span>词汇不当</div>
        <div class="legend-item"><span class="legend-dot bg-gram"></span>语法错误</div>
        <div class="legend-item"><span class="legend-dot bg-corr"></span>修正建议</div>
        <div class="legend-item"><span class="legend-dot bg-inser"></span>遗漏补全</div>
        <div class="legend-item"><span class="legend-symbol-block">...</span>语气词</div>
        <div class="legend-item">
          <span class="legend-symbol-block" style="display: inline-flex; align-items: center; justify-content: center; height: 17px; width: 24px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="color: var(--color-slate-cyan);"><rect x="14" y="4" width="4" height="16" rx="1"></rect><rect x="6" y="4" width="4" height="16" rx="1"></rect></svg>
          </span>
          长停顿
        </div>
      </div>
    </div>

    <!-- Error Details List -->
    <div class="section-card error-details-card" v-if="realErrors.length > 0">
      <h3 class="section-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="title-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        纠错明细 (Details)
      </h3>
      <div class="error-list">
        <div 
          v-for="(err, idx) in realErrors" 
          :key="idx" 
          class="error-detail-item"
        >
          <span :class="['error-type-tag', `tag-${err.status}`]">
            {{ getErrorZh(err.status) }}
          </span>
          <span class="error-desc-text">
            将 "<strong>{{ err.text }}</strong>" 修正为 "<strong>{{ err.correction }}</strong>"
          </span>
        </div>
      </div>
    </div>

    <!-- Deep Analysis -->
    <div class="deep-analysis-section" v-if="spokenResult.deep_analysis">
      <h3 class="da-main-title">口语深度句法剖析 (Deep Analysis)</h3>
      
      <div class="da-grid">
        <!-- Translation -->
        <div class="da-card full-width">
          <h4 class="da-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="da-icon"><path d="m5 8 6 6 6-6"></path><path d="m4 14 6-6 8 8"></path></svg>
            1. 意译与直译对照 (Translation)
          </h4>
          <div class="da-card-content">
            <p class="trans-item"><strong>意译（信达雅）：</strong>{{ spokenResult.deep_analysis.translation }}</p>
            <p v-if="spokenResult.deep_analysis.literal_translation" class="trans-item literal-trans">
              <strong>直译参考：</strong>{{ spokenResult.deep_analysis.literal_translation }}
            </p>
          </div>
        </div>

        <!-- Semantic Chunking -->
        <div class="da-card full-width">
          <h4 class="da-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="da-icon"><line x1="4" y1="9" x2="20" y2="9"></line><line x1="4" y1="15" x2="20" y2="15"></line><line x1="10" y1="3" x2="8" y2="21"></line><line x1="16" y1="3" x2="14" y2="21"></line></svg>
            2. 意群拆分与对照 (Semantic Chunking)
          </h4>
          <div class="da-card-content chunking-grid">
            <div 
              v-for="(chunk, idx) in spokenResult.deep_analysis.chunking" 
              :key="idx" 
              class="chunk-item-wrapper"
            >
              <div class="chunk-box">
                <span class="chunk-en">{{ chunk.english }}</span>
                <span class="chunk-zh">{{ chunk.chinese }}</span>
              </div>
              <span v-if="idx < spokenResult.deep_analysis.chunking.length - 1" class="chunk-separator">/</span>
            </div>
          </div>
        </div>

        <!-- Key Vocabulary -->
        <div class="da-card">
          <h4 class="da-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="da-icon"><circle cx="12" cy="12" r="10"></circle><path d="m9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            3. 重点词汇与短语 (Key Vocabulary)
          </h4>
          <div class="da-card-content">
            <div 
              v-for="(item, idx) in spokenResult.deep_analysis.vocabulary" 
              :key="idx" 
              class="vocab-item"
            >
              <div class="vocab-header">
                <span class="vocab-word">{{ item.word }}</span>
                <span class="vocab-pos">{{ item.pos }}</span>
                <span class="vocab-meaning">{{ item.meaning }}</span>
              </div>
              <p v-if="item.extra" class="vocab-extra">{{ item.extra }}</p>
            </div>
          </div>
        </div>

        <!-- Syntax Analysis -->
        <div class="da-card">
          <h4 class="da-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="da-icon"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="M12 6v6l4 2"></path></svg>
            4. 语法骨架剖析 (Syntax Analysis)
          </h4>
          <div class="da-card-content syntax-content">
            <p><strong>核心主干：</strong>{{ spokenResult.deep_analysis.syntax.skeleton }}</p>
            <p class="syntax-modifiers"><strong>修饰枝叶：</strong>{{ spokenResult.deep_analysis.syntax.modifiers }}</p>
            <p v-if="spokenResult.deep_analysis.syntax.logic">
              <strong>逻辑难点：</strong>{{ spokenResult.deep_analysis.syntax.logic }}
            </p>
          </div>
        </div>

        <!-- Mentor Summary -->
        <div class="da-card full-width summary-card">
          <h4 class="da-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="da-icon" style="color: #f59e0b;"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"></path><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line></svg>
            5. 口语导师小结 (Mentor's Summary)
          </h4>
          <div class="da-card-content mentor-summary-text">
            {{ spokenResult.deep_analysis.summary }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()
const spokenResult = computed(() => store.spokenResult)

const realErrors = computed(() => {
  if (!spokenResult.value || !spokenResult.value.segments) return []
  return spokenResult.value.segments.filter(
    s => s.status === 'pronunciation' || s.status === 'vocabulary' || s.status === 'grammar'
  )
})

function getErrorTitle(status) {
  if (status === 'pronunciation') return '发音问题'
  if (status === 'vocabulary') return '用词不当'
  if (status === 'grammar') return '语法错误'
  return ''
}

function getErrorZh(status) {
  if (status === 'pronunciation') return '发音'
  if (status === 'vocabulary') return '用词'
  if (status === 'grammar') return '语法'
  return ''
}
</script>

<style scoped>
.spoken-feedback {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  background: var(--color-surface);
  border: 1px solid var(--color-sage);
  border-radius: var(--radius-card);
  padding: 24px;
  box-shadow: var(--shadow-subtle);
}

.section-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.title-icon {
  color: var(--color-hudson-blue);
}

.text-display {
  font-family: var(--font-ui);
  font-size: 1.15rem;
  line-height: 1.8;
  color: var(--color-ink);
  padding: 16px 20px;
  background: var(--color-canvas);
  border-radius: 12px;
  border: 1px solid var(--color-sage);
  margin-bottom: 20px;
}

.word-wrapper {
  display: inline-block;
  position: relative;
  margin-right: 0.35em;
}

.word-normal {
  color: var(--color-ink);
}

.word-deleted {
  color: #888888;
  opacity: 0.6;
  text-decoration: line-through;
}

.word-filler {
  color: #999999;
  font-style: italic;
  font-size: 0.95em;
}

.word-pause {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin: 0 4px;
}

.word-indistinct {
  border-bottom: 1px dotted #888888;
  color: #888888;
  font-style: italic;
}

.word-insertion {
  background-color: rgba(239, 68, 68, 0.15);
  border: 1px dashed #ef4444;
  color: #ef4444;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
}

.error-wrapper {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  vertical-align: middle;
  border-radius: 6px;
  padding: 2px 4px;
  background: rgba(0, 0, 0, 0.02);
}

.word-error {
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 500;
}

.bg-pronunciation {
  background-color: rgba(245, 158, 11, 0.15);
  border: 1px solid #f59e0b;
  color: #d97706;
}

.bg-vocabulary {
  background-color: rgba(16, 185, 129, 0.15);
  border: 1px solid #10b981;
  color: #059669;
}

.bg-grammar {
  background-color: rgba(59, 130, 246, 0.15);
  border: 1px solid #3b82f6;
  color: #2563eb;
}

.word-correction {
  font-size: 0.85em;
  background-color: rgba(6, 182, 212, 0.15);
  border: 1px solid #06b6d4;
  color: #0891b2;
  padding: 1px 4px;
  border-radius: 3px;
  margin-top: 4px;
  font-weight: 500;
  letter-spacing: 0;
}

/* Legend Panel */
.legend-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: var(--color-steel);
  border-top: 1px solid var(--color-sage);
  padding-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.bg-pron { background: #f59e0b; }
.bg-vocab { background: #10b981; }
.bg-gram { background: #3b82f6; }
.bg-corr { background: #06b6d4; }
.bg-inser { background: rgba(239, 68, 68, 0.6); }

.legend-symbol-block {
  font-family: monospace;
  background: var(--color-canvas);
  border: 1px solid var(--color-sage);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 11px;
}

/* Error Details List */
.error-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.error-detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: var(--color-canvas);
  border: 1px solid var(--color-sage);
  border-radius: 8px;
}

.error-type-tag {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  color: white;
}

.tag-pronunciation { background: #f59e0b; }
.tag-vocabulary { background: #10b981; }
.tag-grammar { background: #3b82f6; }

.error-desc-text {
  font-size: 14px;
  color: var(--color-ink);
}

/* Deep Analysis Section */
.da-main-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-ink);
  margin-top: 12px;
  margin-bottom: 20px;
}

.da-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.da-card {
  background: var(--color-surface);
  border: 1px solid var(--color-sage);
  border-radius: var(--radius-card);
  padding: 24px;
  box-shadow: var(--shadow-subtle);
}

.da-card-title {
  font-family: var(--font-ui);
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.da-icon {
  color: var(--color-slate-cyan);
}

.da-card-content {
  color: var(--color-ink);
  line-height: 1.6;
}

.trans-item {
  font-size: 15px;
  margin-bottom: 8px;
}
.literal-trans {
  color: var(--color-steel);
  font-size: 14px;
}

/* Chunking Grid */
.chunking-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
.chunking-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: center;
}
.chunk-item-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}
.chunk-box {
  background: var(--color-canvas);
  border: 1px solid var(--color-sage);
  border-radius: 12px;
  padding: 10px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.chunk-en {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-hudson-blue);
}
.chunk-zh {
  font-size: 13px;
  color: var(--color-steel);
}
.chunk-separator {
  color: var(--color-sage);
  font-size: 18px;
  font-weight: 300;
}

/* Key Vocabulary */
.vocab-item {
  border-bottom: 1px solid var(--color-sage);
  padding-bottom: 12px;
  margin-bottom: 12px;
}
.vocab-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}
.vocab-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}
.vocab-word {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
}
.vocab-pos {
  font-size: 13px;
  font-style: italic;
  color: var(--color-steel);
}
.vocab-meaning {
  font-size: 14px;
  color: var(--color-ink);
}
.vocab-extra {
  font-size: 13px;
  color: var(--color-steel);
  margin-top: 4px;
}

/* Syntax Content */
.syntax-content {
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.syntax-modifiers {
  line-height: 1.6;
}

/* Mentor Summary */
.summary-card {
  border-left: 4px solid #f59e0b;
}
.mentor-summary-text {
  font-size: 15px;
  line-height: 1.7;
  color: var(--color-carbon);
}
</style>
