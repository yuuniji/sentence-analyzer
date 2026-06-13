<template>
  <div class="markdown-body" @click="handleTabClick" v-html="renderedHtml"></div>
</template>

<script setup>
import { computed, watch, nextTick, onMounted } from 'vue'
import { renderMarkdown } from '../utils/markdown-renderer'
import { useAnalyzerStore } from '../stores/analyzer'

const store = useAnalyzerStore()

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

const renderedHtml = computed(() => {
  return renderMarkdown(props.content)
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
  containers.forEach(container => {
    const placeholder = container.querySelector('.tabs-nav-placeholder')
    if (!placeholder) return
    
    const panes = container.querySelectorAll('.tab-pane')
    if (panes.length === 0) return
    
    let navHtml = '<div class="tabs-nav">'
    panes.forEach((pane, index) => {
      const title = pane.getAttribute('data-title') || `Tab ${index + 1}`
      // preserve active state if already set (during streaming)
      const isActive = pane.classList.contains('active') || (index === 0 && !container.querySelector('.tab-pane.active'))
      navHtml += `<button class="tab-button ${isActive ? 'active' : ''}" data-index="${index}">${title}</button>`
      if (isActive) pane.classList.add('active')
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

  if (e.target.classList.contains('tab-button')) {
    const btn = e.target
    const container = btn.closest('.tabs-container')
    const index = btn.getAttribute('data-index')
    
    // Update buttons
    container.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'))
    btn.classList.add('active')
    
    // Update panes
    container.querySelectorAll('.tab-pane').forEach((p, i) => {
      if (i.toString() === index) {
        p.classList.add('active')
      } else {
        p.classList.remove('active')
      }
    })
  }
}
</script>
