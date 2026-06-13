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

    <!-- 口语评估录音区 -->
    <div v-else-if="store.activeEngine === 'spoken'" class="spoken-wrapper animate-fade-in">
      <div class="recorder-card">
        <div class="recorder-title" style="display: flex; align-items: center; justify-content: center; gap: 8px;">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--color-slate-cyan); flex-shrink: 0;"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="22"></line></svg>
          <span>口语语法与发音评估</span>
        </div>
        <div class="recorder-desc">点击下方按钮开始录音，说出你的英语口语。录制结束后，可以试听并提交 AI 进行多维度纠错评估。</div>
        
        <div class="recorder-controls">
          <button 
            :class="['record-btn', { 'recording': isRecording }]" 
            @click="toggleRecording"
            :disabled="store.isUploading"
          >
            <div class="mic-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="22"></line></svg>
            </div>
            <span class="btn-text">{{ isRecording ? '点击停止录音' : '点击开始录音' }}</span>
            <span v-if="isRecording" class="timer">{{ formattedTime }}</span>
          </button>
        </div>

        <div v-if="audioURL" class="audio-preview-box">
          <audio :src="audioURL" controls class="custom-audio-player"></audio>
          <button 
            class="analyze-btn" 
            @click="submitSpokenAnalysis" 
            :disabled="store.isUploading"
          >
            <span>{{ store.isUploading ? '口语解析中...' : '开始口语评估' }}</span>
            <svg v-if="!store.isUploading" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"></path><path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5Z"></path><path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1Z"></path></svg>
          </button>
        </div>
      </div>
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
          <div class="hint-text" style="display: inline-flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--color-slate-cyan); flex-shrink: 0;"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"></path><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line></svg>
            <span>提示：保留原文排版可提升解析精度，例如 <code>*斜体*</code> 或 <code>**加粗**</code></span>
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
    
    <div v-if="store.activeEngine !== 'spoken'" class="controls">
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
        <span>{{ store.isStreaming ? '正在解析...' : '开始解析' }}</span>
        <svg v-if="!store.isStreaming" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"></path><path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5Z"></path><path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1Z"></path></svg>
      </button>
    </div>
    
    <div v-if="store.errorMessage" class="error-msg">
      {{ store.errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()
const showAdvanced = ref(false)

// 录音相关状态
const isRecording = ref(false)
const recordingDuration = ref(0)
const audioURL = ref(null)
const audioBlob = ref(null)

let mediaRecorder = null
let audioChunks = []
let timerInterval = null

const formattedTime = computed(() => {
  const mins = Math.floor(recordingDuration.value / 60).toString().padStart(2, '0')
  const secs = (recordingDuration.value % 60).toString().padStart(2, '0')
  return `${mins}:${secs}`
})

async function toggleRecording() {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    audioURL.value = null
    audioBlob.value = null
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }
    
    mediaRecorder.onstop = () => {
      const mimeType = mediaRecorder.mimeType || 'audio/webm'
      audioBlob.value = new Blob(audioChunks, { type: mimeType })
      audioURL.value = URL.createObjectURL(audioBlob.value)
    }
    
    mediaRecorder.start()
    isRecording.value = true
    recordingDuration.value = 0
    
    timerInterval = setInterval(() => {
      recordingDuration.value++
    }, 1000)
    
  } catch (err) {
    console.error("Microphone access error", err)
    alert("无法访问麦克风，请检查浏览器权限。")
  }
}

function stopRecording() {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
    clearInterval(timerInterval)
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
  }
}

function submitSpokenAnalysis() {
  if (audioBlob.value) {
    store.uploadAudio(audioBlob.value)
  }
}

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
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 24px;
  background: var(--color-surface-nav); /* Dark fill */
  color: #ffffff;
  border: none;
  border-radius: var(--radius-btn);
  font-weight: 500;
  font-size: 15px;
  transition: all 0.2s;
  cursor: pointer;
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

/* Spoken Recorder styling */
.spoken-wrapper {
  padding: 10px 0;
}
.recorder-card {
  background: var(--color-surface);
  border: 1px dashed var(--color-sage);
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.recorder-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
}
.recorder-desc {
  font-size: 14px;
  color: var(--color-steel);
  max-width: 450px;
  line-height: 1.5;
}
.recorder-controls {
  margin: 16px 0;
}
.record-btn {
  background: var(--color-surface-nav);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 14px 28px;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-subtle);
}
.record-btn:hover {
  opacity: 0.9;
  transform: scale(1.02);
}
.record-btn.recording {
  background: #ef4444;
  animation: pulse-red 1.5s infinite;
}
.mic-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}
.timer {
  font-family: monospace;
  font-size: 15px;
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 8px;
  border-radius: 4px;
}
.audio-preview-box {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}
.custom-audio-player {
  width: 100%;
  max-width: 400px;
}
@keyframes pulse-red {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}
</style>
