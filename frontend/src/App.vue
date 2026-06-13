<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo">
        <h1>🔍 英语长难句智能解析</h1>
      </div>
      <div class="header-actions">
        <!-- Settings btn could go here -->
      </div>
    </header>
    
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
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0 30px 0;
}

.logo h1 {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
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
  gap: 24px;
  overflow-y: auto;
  padding-right: 10px;
  padding-bottom: 40px;
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
