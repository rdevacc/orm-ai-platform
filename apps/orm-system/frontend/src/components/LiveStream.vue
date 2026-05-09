<template>
  <div class="mode-container">
    <div class="view-panel">
      <video ref="video" autoplay playsinline class="media-element"></video>
      <canvas ref="overlay" class="canvas-overlay"></canvas>
      <!-- Indikator mode yang aktif -->
      <div class="ai-badge" v-if="isDetecting">
        SYSTEM ACTIVE ({{ mode.toUpperCase() }})
      </div>
    </div>
    <div class="action-bar">
      <button @click="toggleDetection" :class="isDetecting ? 'btn-stop' : 'btn-start'">
        {{ isDetecting ? 'ABORT PROCESS' : 'EXECUTE DETECTION' }}
      </button>
    </div>
    <canvas ref="captureCanvas" v-show="false" width="640" height="480"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps } from 'vue'
import axios from 'axios'

// Menambahkan props untuk menerima pilihan mode dari App.vue
const props = defineProps({
  mode: {
    type: String,
    default: 'fast'
  }
})

const emit = defineEmits(['update-detections'])
const video = ref(null)
const overlay = ref(null)
const captureCanvas = ref(null)
const isDetecting = ref(false)
const cameraError = ref(false)

onMounted(async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (video.value) {
      video.value.srcObject = stream
      cameraError.value = false
    }
  } catch (err) {
    cameraError.value = true
    console.error("Hardware Error:", err)
    if (err.name === 'NotAllowedError') {
       alert("Akses kamera ditolak. Fitur Live Stream tidak akan berfungsi.")
    }
  }
})

onUnmounted(() => {
  if (video.value?.srcObject) {
    video.value.srcObject.getTracks().forEach(t => t.stop())
  }
})

const toggleDetection = () => {
  isDetecting.value = !isDetecting.value
  if (!isDetecting.value) {
    const canvas = overlay.value
    if (canvas) {
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  } else {
    runInferenceCycle()
  }
}

const runInferenceCycle = async () => {
  if (!isDetecting.value) return
  
  const ctx = captureCanvas.value.getContext('2d')
  ctx.drawImage(video.value, 0, 0, 640, 480)
  
  captureCanvas.value.toBlob(async (blob) => {
    const formData = new FormData()
    formData.append('file', blob)
    try {
      const res = await axios.post(`https://aidetection.mektan.my.id/detect?mode=${props.mode}`, formData)
      
      const results = res.data.results
      emit('update-detections', results)
      drawVisualOverlay(results)
    } catch (e) {
      console.error("Inference Error:", e)
    }
    
    // Memberikan jeda sedikit agar tidak membebani browser/server
    setTimeout(runInferenceCycle, 250)
  }, 'image/jpeg', 0.8)
}

const drawVisualOverlay = (results) => {
  const canvas = overlay.value
  const videoEl = video.value;
  if (!canvas || !videoEl) return
  const ctx = canvas.getContext('2d')
  
  canvas.width = videoEl.clientWidth;
  canvas.height = videoEl.clientHeight;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  const scaleX = canvas.width / videoEl.videoWidth;
  const scaleY = canvas.height / videoEl.videoHeight;

  results.forEach(d => {
    const [x1, y1, x2, y2] = d.bbox
    const confidence = Math.round(d.confidence * 100) + '%'
    const label = `${d.class.toUpperCase()} ${confidence}`

    const rectX = x1 * scaleX;
    const rectY = y1 * scaleY;
    const rectW = (x2 - x1) * scaleX;
    const rectH = (y2 - y1) * scaleY;

    ctx.strokeStyle = '#00ff41'
    ctx.lineWidth = 3
    ctx.strokeRect(rectX, rectY, rectW, rectH);

    ctx.font = 'bold 12px monospace'
    const textWidth = ctx.measureText(label).width
    ctx.fillStyle = '#00ff41'
    ctx.fillRect(rectX, rectY - 20, textWidth + 10, 20)

    ctx.fillStyle = '#000000'
    ctx.fillText(label, rectX + 5, rectY - 5)
  })
}
</script>

<style scoped>
.view-panel { position: relative; background: #000; border: 1px solid #333; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; overflow: hidden; border-radius: 12px; }
.media-element { width: 100%; height: 100%; object-fit: fill; }
.canvas-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.ai-badge { position: absolute; top: 15px; right: 15px; background: #ff003c; color: white; padding: 5px 12px; font-size: 0.7rem; font-weight: bold; animation: blink 1s infinite; border-radius: 4px; z-index: 10; }
@keyframes blink { 50% { opacity: 0.3; } }
.action-bar { display: flex; justify-content: center;}
button { margin-top:30px; padding: 15px 35px; cursor: pointer; font-weight: bold; border: none; text-transform: uppercase; transition: 0.3s; border-radius: 12px; }
.btn-start { background: #00ff41; color: #000; }
.btn-stop { background: #ff003c; color: white; }
</style>