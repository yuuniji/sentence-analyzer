<template>
  <div class="app-container">
    <nav class="floating-nav">
      <div class="nav-links">
        <button 
          :class="['nav-item', { active: store.activeEngine === 'sentence' }]"
          @click="store.activeEngine = 'sentence'"
        >长难句精读</button>
        <button 
          :class="['nav-item', { active: store.activeEngine === 'article' }]"
          @click="store.activeEngine = 'article'"
        >篇章导读</button>
        <button 
          :class="['nav-item', { active: store.activeEngine === 'spoken' }]"
          @click="store.activeEngine = 'spoken'"
        >口语评估</button>
      </div>
      <div class="nav-divider"></div>
      <a 
        href="https://github.com/yuuniji" 
        target="_blank" 
        rel="noopener noreferrer" 
        class="github-link" 
        title="GitHub"
      >
        <svg viewBox="0 0 16 16" width="18" height="18" class="github-icon">
          <path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
        </svg>
      </a>
    </nav>
    
    <main class="app-main">
      <div class="sidebar">
        <HistoryPanel />
      </div>
      <div class="content-area">
        <InputPanel />
        <transition name="fade">
          <OutputPanel v-if="store.hasOutput" class="animate-fade-in" />
        </transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useAnalyzerStore } from './stores/analyzer'
import InputPanel from './components/InputPanel.vue'
import OutputPanel from './components/OutputPanel.vue'
import HistoryPanel from './components/HistoryPanel.vue'

const store = useAnalyzerStore()
</script>

<style scoped>
.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 20px 20px 20px; /* Added top padding to account for floating nav */
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Floating Pill Navigation */
.floating-nav {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: var(--color-surface-nav); /* Graphite Night */
  border-radius: var(--radius-pill);
  padding: 4px;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-nav);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-item {
  background: transparent;
  border: none;
  color: #a5afaf; /* Ash */
  font-size: 15px;
  font-weight: 500;
  padding: 6px 16px;
  border-radius: var(--radius-pill);
  transition: all 0.2s;
}

.nav-item:hover {
  color: #ffffff;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-divider {
  width: 1px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.15);
  margin: 0 8px 0 12px;
}

.github-link {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a5afaf; /* Ash */
  padding: 8px;
  margin-right: 4px;
  border-radius: var(--radius-pill);
  transition: all 0.2s ease;
}

.github-link:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

.github-icon {
  display: block;
}

.app-main {
  display: flex;
  gap: 24px;
  flex-grow: 1;
  min-height: 0; /* Important for scrollable children */
}

.sidebar {
  width: 320px;
  flex-shrink: 0;
}

.content-area {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  padding-right: 10px;
  padding-bottom: 40px;
}

/* Prevent flex children from being compressed — they must render at natural height */
.content-area > * {
  flex-shrink: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 900px) {
  .app-main {
    flex-direction: column-reverse;
  }
  .sidebar {
    width: 100%;
    height: 300px;
  }
}
</style>
