<template>
  <div class="mode-container">
    <div class="view-panel">
      <div v-if="!imagePreview" class="upload-placeholder">
        <input type="file" @change="handleFileUpload" id="fileInput" accept="image/*" hidden />
        <label for="fileInput" class="upload-label">
          <span class="upload-icon">📁</span>
          <p>DROP FILE OR CLICK TO SCAN</p>
        </label>
      </div>
      <div v-else class="preview-wrapper">
        <img :src="imagePreview" class="media-element" ref="previewImg" @load="handleImageLoad" />
        <canvas ref="uploadOverlay" class="canvas-overlay"></canvas>
      </div>
    </div>

    <div class="action-bar">
      <button v-if="imagePreview" @click="resetUpload" class="btn-secondary">CLEAR</button>
      <button v-if="imagePreview" @click="processImage" class="btn-start" :disabled="isProcessing || isCompressing">
        <!-- Teks berubah sesuai status -->
        <span v-if="isCompressing">PREPARING IMAGE...</span>
        <span v-else-if="isProcessing">ANALYZING...</span>
        <span v-else>RUN DIAGNOSTICS</span>
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import imageCompression from 'browser-image-compression'

  const emit = defineEmits(['update-detections'])
  const imagePreview = ref(null)
  const selectedFile = ref(null)
  const isProcessing = ref(false)
  const uploadOverlay = ref(null)
  const previewImg = ref(null)
  const isCompressing = ref(false)

  // Menyimpan dimensi gambar hasil kompresi (referensi koordinat AI)
  const analyzedDimensions = ref({ width: 0, height: 0 })

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // 1. Langsung tampilkan preview gambar asli agar responsif
    imagePreview.value = URL.createObjectURL(file)
    isCompressing.value = true
    
    // 2. Konfigurasi Kompresi
    const options = {
      maxSizeMB: 1,
      maxWidthOrHeight: 1280,
      useWebWorker: true
    }

    try {
      const compressedFile = await imageCompression(file, options)
      selectedFile.value = compressedFile

      // 3. Ambil dimensi gambar hasil kompresi untuk perhitungan box nanti
      const bitmap = await createImageBitmap(compressedFile)
      analyzedDimensions.value = { width: bitmap.width, height: bitmap.height }
      
      console.log(`Ready: ${analyzedDimensions.value.width}x${analyzedDimensions.value.height}`)
    } catch (error) {
      console.error("Compression Error:", error)
      selectedFile.value = file
    } finally {
      isCompressing.value = false
    }

    emit('update-detections', [])
  }

  const handleImageLoad = () => {
    const canvas = uploadOverlay.value
    if (canvas) {
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }

  const processImage = async () => {
    if (!selectedFile.value) return
    
    isProcessing.value = true
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    try {
      const res = await axios.post('https://aidetection.mektan.my.id/detect?mode=accurate', formData);
      const results = res.data.results
      emit('update-detections', results)
      
      // Tunggu DOM update sebentar sebelum menggambar box
      setTimeout(() => drawBoxes(results), 50)
    } catch (e) {
      console.error("Static Analysis Error:", e)
      alert("Analisis gagal. Pastikan file tidak terlalu besar.")
    } finally {
      isProcessing.value = false
    }
  }

  const drawBoxes = (results) => {
    const canvas = uploadOverlay.value
    const img = previewImg.value
    if (!canvas || !img || !analyzedDimensions.value.width) return

    const ctx = canvas.getContext('2d')

    // Samakan dimensi canvas dengan ukuran gambar yang tampil di layar
    canvas.width = img.clientWidth
    canvas.height = img.clientHeight
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Hitung rasio antara gambar hasil kompresi (yang dibaca AI) dan tampilan layar
    const scaleX = canvas.width / analyzedDimensions.value.width
    const scaleY = canvas.height / analyzedDimensions.value.height

    results.forEach(d => {
      const [x1, y1, x2, y2] = d.bbox
      
      // Transformasi koordinat
      const rx = x1 * scaleX
      const ry = y1 * scaleY
      const rw = (x2 - x1) * scaleX
      const rh = (y2 - y1) * scaleY

      // Gambar Bounding Box
      ctx.strokeStyle = '#00ff41'
      ctx.lineWidth = 3
      ctx.strokeRect(rx, ry, rw, rh)

      // Gambar Label
      const confidence = Math.round(d.confidence * 100) + '%'
      const labelText = `${d.class.toUpperCase()} ${confidence}`
      
      ctx.font = 'bold 12px monospace'
      const textWidth = ctx.measureText(labelText).width
      
      // Background Label
      ctx.fillStyle = '#00ff41'
      ctx.fillRect(rx, ry - 20, textWidth + 10, 20)

      // Teks Label
      ctx.fillStyle = '#000000'
      ctx.fillText(labelText, rx + 5, ry - 5)
    })
  }

  const resetUpload = () => {
    imagePreview.value = null
    selectedFile.value = null
    analyzedDimensions.value = { width: 0, height: 0 }
    emit('update-detections', [])
  }
</script>

<style scoped>
  .mode-container { width: 100%; display: flex; flex-direction: column; align-items: center; }

  .view-panel { 
    position: relative; 
    background: #0a0a0a; 
    border: 1px solid #333; 
    width: 100%;
    max-width: 800px;
    height: 450px;
    margin: 0 auto;
    display: flex; 
    align-items: center; 
    justify-content: center; 
    overflow: hidden;
  }

  .preview-wrapper { 
    position: relative; 
    max-width: 100%;
    max-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .media-element { 
    max-width: 100%; 
    max-height: 450px;
    width: auto;
    height: auto;
    object-fit: contain; 
    display: block;
  }

  .canvas-overlay { 
    position: absolute; 
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }

  .upload-label { cursor: pointer; text-align: center; color: #444; transition: 0.3s; }
  .upload-label:hover { color: #00ff41; }
  .upload-icon { font-size: 4rem; display: block; margin-bottom: 30px; }

  .action-bar { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }

  button { 
    padding: 12px 30px; 
    cursor: pointer; 
    font-weight: bold; 
    border: none; 
    text-transform: uppercase; 
  }

  .btn-start { background: #00ff41; color: #000; }
  .btn-secondary { background: #222; color: #eee; border: 1px solid #444; }
  button:disabled { background: #555; cursor: not-allowed; opacity: 0.6; }
</style>