<template>
  <div class="markdown-body" @click="handleTabClick" v-html="renderedHtml"></div>
</template>

<script setup>
import { computed, watch, nextTick, ref, onMounted } from 'vue'
import { renderMarkdown } from '../utils/markdown-renderer'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()
const activeTabsMap = ref(new Map())

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

const renderedHtml = computed(() => {
  return renderMarkdown(props.content)
})

// When starting a new parse (content is cleared), we should clear the map
watch(() => props.content, (newVal, oldVal) => {
  if (!newVal || newVal.length < oldVal?.length / 2) {
    activeTabsMap.value.clear()
  }
})

watch(renderedHtml, () => {
  nextTick(() => {
    buildTabs()
  })
}, { immediate: true })

onMounted(() => {
  nextTick(() => {
    buildTabs()
  })
})

function buildTabs() {
  const containers = document.querySelectorAll('.tabs-container')
  containers.forEach((container, cIndex) => {
    const placeholder = container.querySelector('.tabs-nav-placeholder')
    if (!placeholder) return
    
    const panes = container.querySelectorAll('.tab-pane')
    if (panes.length === 0) return
    
    const activeIdx = activeTabsMap.value.get(cIndex) || 0
    
    let navHtml = '<div class="tabs-nav">'
    panes.forEach((pane, index) => {
      const title = pane.getAttribute('data-title') || `Tab ${index + 1}`
      const isActive = index === activeIdx
      navHtml += `<button class="tab-button ${isActive ? 'active' : ''}" data-index="${index}" data-cindex="${cIndex}">${title}</button>`
      if (isActive) {
        pane.classList.add('active')
      } else {
        pane.classList.remove('active')
      }
    })
    navHtml += '</div>'
    
    placeholder.outerHTML = navHtml
  })
}

function handleTabClick(e) {
  // Handle Radar Button clicks
  const radarBtn = e.target.closest('.radar-btn')
  if (radarBtn) {
    const sentence = radarBtn.getAttribute('data-sentence')
    if (sentence) {
      store.switchToSentence(sentence)
    }
    return
  }

  // Handle Tab clicks
  if (e.target.classList.contains('tab-button')) {
    const btn = e.target
    const container = btn.closest('.tabs-container')
    const index = parseInt(btn.getAttribute('data-index'))
    const cIndex = parseInt(btn.getAttribute('data-cindex'))
    
    // Save to map so it survives stream re-renders
    activeTabsMap.value.set(cIndex, index)
    
    // Update DOM instantly for snappiness
    container.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'))
    btn.classList.add('active')
    
    container.querySelectorAll('.tab-pane').forEach((p, i) => {
      if (i === index) {
        p.classList.add('active')
      } else {
        p.classList.remove('active')
      }
    })
  }
}
</script>
