<template>
  <div class="app-container">
    <TheHeader />

    <!-- TAB NAV -->
    <nav class="tab-nav">
      <button @click="switchTab('live')" :class="{ active: activeTab === 'live' }">REAL-TIME STREAM</button>
      <button @click="switchTab('upload')" :class="{ active: activeTab === 'upload' }">IMAGE ANALYSIS</button>
    </nav>

    <!-- MODEL SELECTOR -->
    <div class="model-selector-container">
      <span class="label">AI ENGINE:</span>
      <select v-model="selectedMode" class="model-select">
        <option value="fast">Fast Mode (YOLOv8n)</option>
        <option value="accurate">Accurate Mode (YOLOv8m)</option>
        <option value="custom_model">Custom Model (YOLOv8)</option>
      </select>
    </div>

    <main class="content-card">
      <!-- Kita kirim 'mode' sebagai props ke komponen anak -->
      <LiveStream 
        v-if="activeTab === 'live'" 
        :mode="selectedMode"
        @update-detections="handleResults" 
      />
      
      <ImageAnalysis 
        v-if="activeTab === 'upload'" 
        :mode="selectedMode"
        @update-detections="handleResults" 
      />
      
      <MetadataPanel :detections="currentResults" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TheHeader from './components/TheHeader.vue'
import LiveStream from './components/LiveStream.vue'
import ImageAnalysis from './components/ImageAnalysis.vue'
import MetadataPanel from './components/MetadataPanel.vue'

const activeTab = ref('live')
const selectedMode = ref('fast') // Default mode
const currentResults = ref([])

const handleResults = (results) => {
  currentResults.value = results
}

const switchTab = (tabName) => {
  activeTab.value = tabName
  currentResults.value = [] 
}
</script>

<style>
/* Tambahkan style untuk Model Selector */
.model-selector-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.model-selector-container .label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #00ff41;
  letter-spacing: 1px;
}

.model-select {
  background: #1a1a1e;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 8px;
  outline: none;
  cursor: pointer;
  font-family: inherit;
  transition: border 0.3s;
}

.model-select:focus {
  border-color: #00ff41;
}

/* Reset & Global */
body { margin: 0; padding: 0; background: #0a0a0c; }

.app-container { 
  min-height: 100vh; 
  background: #0a0a0c; 
  color: #e2e8f0; 
  font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
  padding-bottom: 50px; 
}

.content-card { max-width: 900px; margin: 0 auto; padding: 0 20px; }

/* TAB NAV STYLE - Round Modern Edition */
.tab-nav { 
  display: flex; 
  justify-content: center; 
  gap: 12px; 
  margin: 30px 0; 
  background: rgba(255, 255, 255, 0.03);
  padding: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.tab-nav button { 
  padding: 10px 24px; 
  border: none; 
  background: transparent; 
  color: #666; 
  cursor: pointer; 
  transition: all 0.3s ease; 
  font-weight: 600;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
  border-radius: 40px;
}

.tab-nav button.active { 
  background: #00ff41; 
  color: #000; 
  box-shadow: 0 4px 15px rgba(0, 255, 65, 0.3);
}

.tab-nav button:hover:not(.active) {
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
}

/* Global Button Styles (Untuk Start/Stop/Action) */
button {
  position: relative;
  padding: 12px 32px;
  background: transparent;
  color: #fff;
  border: 2px solid rgba(0, 255, 65, 0.3);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  border-radius: 12px; /* Round Modern Style */
}

button:hover {
  background: rgba(0, 255, 65, 0.1);
  border-color: #00ff41;
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
  transform: translateY(-2px);
}

.btn-start { 
  border-color: #00ff41; 
  color: #00ff41; 
}

.btn-stop { 
  border-color: #ff003c; 
  color: #ff003c; 
}

.btn-stop:hover { 
  background: rgba(255, 0, 60, 0.1); 
  border-color: #ff003c;
  box-shadow: 0 0 20px rgba(255, 0, 60, 0.2); 
}

.btn-secondary {
  border-color: #444;
  color: #888;
  border-radius: 12px;
}
</style>