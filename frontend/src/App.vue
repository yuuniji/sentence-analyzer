<template>
  <div class="app-container">
    <!-- Floating Pill Navigation -->
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
      </div>
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
