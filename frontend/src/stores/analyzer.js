import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAnalyzerStore = defineStore('analyzer', () => {
  // 状态
  const inputSentence = ref('')
  const inputContext = ref('')
  const outputMarkdown = ref('')
  const isStreaming = ref(false)
  const streamProgress = ref(0)
  const currentRecordId = ref(null)
  const errorMessage = ref('')
  const selectedMode = ref('standard')
  const selectedModel = ref('gemini-2.5-pro')
  const availableModels = ref([])
  
  // 历史记录
  const history = ref([])
  const historyPage = ref(1)
  const historyTotal = ref(0)
  
  // 计算属性
  const hasOutput = computed(() => outputMarkdown.value.length > 0)
  const canAnalyze = computed(
    () => inputSentence.value.trim().length > 0 && !isStreaming.value
  )
  
  // 改进的 SSE 接收逻辑
  async function analyze() {
    if (!canAnalyze.value) return
    
    outputMarkdown.value = ''
    isStreaming.value = true
    errorMessage.value = ''
    
    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sentence: inputSentence.value,
          mode: selectedMode.value,
          model: selectedModel.value,
          context: inputContext.value || undefined
        })
      })
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let currentEvent = 'message'
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) {
          isStreaming.value = false
          break
        }
        
        const chunk = decoder.decode(value, {stream: true})
        const lines = chunk.split('\n')
        
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i]
          if (line.startsWith('event: ')) {
            currentEvent = line.substring(7).trim()
          } else if (line.startsWith('data: ')) {
            const data = line.substring(6)
            if (currentEvent === 'chunk') {
              try {
                const payload = JSON.parse(data)
                if (payload.text) {
                  outputMarkdown.value += payload.text
                } else {
                  outputMarkdown.value += data
                }
              } catch(e) {
                // 兼容旧的非 JSON 数据格式
                outputMarkdown.value += data
                if (i < lines.length - 1 && lines[i+1] === '') {
                   outputMarkdown.value += '\n'
                }
              }
            } else if (currentEvent === 'done') {
              try {
                const json = JSON.parse(data)
                currentRecordId.value = json.record_id
                isStreaming.value = false
                loadHistory(1)
              } catch(e) {}
            } else if (currentEvent === 'error') {
              try {
                 errorMessage.value = JSON.parse(data).message
                 isStreaming.value = false
              } catch(e) {}
            }
          }
        }
      }
    } catch (err) {
      errorMessage.value = err.message
      isStreaming.value = false
    }
  }
  
  async function loadHistory(page = 1) {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/history?page=${page}&page_size=20`)
      history.value = res.data.records
      historyTotal.value = res.data.total
      historyPage.value = page
    } catch (e) {
      console.error('Failed to load history', e)
    }
  }
  
  async function loadModels() {
    try {
      const res = await axios.get('http://127.0.0.1:8000/models')
      availableModels.value = res.data.models
      // 如果当前选中的模型不在列表中，自动重置为一个可用的
      if (availableModels.value.length > 0 && !availableModels.value.find(m => m.name === selectedModel.value)) {
        selectedModel.value = availableModels.value[0].name
      }
    } catch (e) {
      console.error('Failed to load models', e)
    }
  }
  
  function loadRecord(record) {
    inputSentence.value = record.sentence
    inputContext.value = record.context || ''
    outputMarkdown.value = record.output
    currentRecordId.value = record.id
    selectedMode.value = record.mode || 'standard'
  }
  
  async function deleteRecord(id) {
    try {
      await axios.delete(`http://127.0.0.1:8000/history/${id}`)
      if (currentRecordId.value === id) {
        inputSentence.value = ''
        outputMarkdown.value = ''
        currentRecordId.value = null
      }
      loadHistory(historyPage.value)
    } catch (e) {
      console.error('Failed to delete record', e)
    }
  }
  
  return {
    inputSentence, inputContext, outputMarkdown, isStreaming, streamProgress,
    currentRecordId, errorMessage, selectedMode, selectedModel,
    history, historyPage, historyTotal, availableModels,
    hasOutput, canAnalyze,
    analyze, loadHistory, loadRecord, deleteRecord, loadModels
  }
})
