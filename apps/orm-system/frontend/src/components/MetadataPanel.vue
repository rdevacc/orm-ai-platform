<template>
  <div class="metadata-container" v-show="detections.length > 0">
    <div class="panel-header">
      <div class="header-main">
        <span class="status-pulse"></span>
        <h3>DIAGNOSTIC DATA ENGINE</h3>
      </div>
      <span class="object-count">{{ detections.length }} OBJECTS DETECTED</span>
    </div>
    
    <div class="table-wrapper">
      <table class="modern-table">
        <thead>
          <tr>
            <th>CLASS</th>
            <th>CONFIDENCE</th>
            <th>BOUNDING BOX (XYWH)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(d, i) in detections" :key="i" class="data-row">
            <td class="class-name">{{ d.class.toUpperCase() }}</td>
            <td>
              <div class="confidence-wrapper">
                <div class="bar-bg">
                  <div class="bar-fill" :style="{ width: (d.confidence * 100) + '%' }"></div>
                </div>
                <span class="pct">{{ (d.confidence * 100).toFixed(1) }}%</span>
              </div>
            </td>
            <td class="bbox-code">
              {{ formatBBox(d.bbox) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps(['detections'])

// Helper untuk format [x, y, w, h] agar rapi di tabel
const formatBBox = (bbox) => {
  const [x1, y1, x2, y2] = bbox;
  const w = x2 - x1;
  const h = y2 - y1;
  return `[${x1}, ${y1}, ${w}, ${h}]`;
}
</script>

<style scoped>
.metadata-container { 
  margin-top: 30px; 
  background: rgba(10, 10, 12, 0.8); 
  border: 1px solid #1e293b; 
  border-left: 4px solid #00ff41;
  border-radius: 4px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: rgba(30, 41, 59, 0.3);
  border-bottom: 1px solid #1e293b;
}

.header-main { display: flex; align-items: center; gap: 10px; }

.status-pulse {
  width: 8px; height: 8px;
  background: #00ff41;
  border-radius: 50%;
  box-shadow: 0 0 8px #00ff41;
  animation: pulse 1.5s infinite;
}

@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

h3 { margin: 0; font-size: 0.85rem; letter-spacing: 2px; color: #94a3b8; }
.object-count { font-size: 0.7rem; color: #00ff41; font-weight: bold; }

.table-wrapper { overflow-x: auto; }

.modern-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.modern-table th { 
  padding: 12px 20px; 
  text-align: left; 
  color: #64748b; 
  border-bottom: 1px solid #1e293b;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.modern-table td { 
  padding: 12px 20px; 
  border-bottom: 1px solid #0f172a; 
  color: #cbd5e1;
}

.class-name { color: #00ff41; font-weight: bold; }
.bbox-code { font-family: 'Courier New', monospace; color: #64748b; }

.confidence-wrapper { display: flex; align-items: center; gap: 10px; }
.bar-bg { width: 80px; height: 4px; background: #1e293b; border-radius: 2px; overflow: hidden; }
.bar-fill { height: 100%; background: #00ff41; box-shadow: 0 0 5px #00ff41; }
.pct { min-width: 45px; font-variant-numeric: tabular-nums; }

.data-row:hover { background: rgba(0, 255, 65, 0.05); }
</style>