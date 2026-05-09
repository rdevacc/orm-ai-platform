<template>
  <div
    class="bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-xl h-full flex flex-col"
  >

    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">

          <!-- Model Selection -->
      <div
        class="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center"
      >
        📷
      </div>

      <div>

        <h2 class="text-xl font-bold">
          Upload Recognition
        </h2>

        <p class="text-sm text-slate-400 mt-1">
          Analisa wajah menggunakan embedding dan classifier
        </p>

      </div>

      <div class="mb-6">

        <label
          class="block text-sm text-slate-400 mb-2"
        >
          Recognition Model
        </label>

        <select

          v-model="selectedModel"

          class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >

          <option value="embedding">
            Embedding
          </option>

          <option value="classifier">
            Classifier
          </option>

        </select>

      </div>

    </div>

    <!-- Upload Area -->
    <div
      class="border-2 border-dashed border-slate-600 rounded-2xl p-10 text-center hover:border-emerald-500 transition-all duration-300 cursor-pointer"
      @click="openFile"
    >

      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFile"
      />

      <div class="flex flex-col items-center">

        <div
          class="w-16 h-16 rounded-2xl bg-slate-700 flex items-center justify-center text-3xl mb-4"
        >
          🖼️
        </div>

        <h3 class="text-lg font-semibold mb-2">
          Upload Gambar Wajah
        </h3>

        <p class="text-slate-400 text-sm mb-6">
          Klik untuk memilih file gambar
        </p>

        <button
          :disabled="processing"
          class="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:cursor-not-allowed transition-all duration-300 px-6 py-3 rounded-xl font-semibold"
        >

          {{
            processing
              ? 'Processing...'
              : 'Pilih Gambar'
          }}

        </button>

      </div>

    </div>

    <!-- Preview -->
    <div
      v-if="preview"
      class="mt-6"
    >

      <!-- Preview Image -->
      <div
        class="relative overflow-hidden rounded-2xl border border-slate-700 bg-black flex justify-center"
      >

        <img
          ref="previewImage"
          :src="preview"
          class="w-full max-h-[420px] object-contain bg-black"
        />

        <canvas
          ref="overlayCanvas"
          class="absolute inset-0 pointer-events-none"
        ></canvas>

      </div>

      <!-- File Info -->
      <div
        class="mt-4 bg-slate-900 border border-slate-700 rounded-xl p-4"
      >

        <div class="flex items-center justify-between text-sm">

          <div>

            <p class="text-slate-400 mb-1">
              File
            </p>

            <p class="font-medium break-all">
              {{ fileName }}
            </p>

          </div>

          <div class="text-right">

            <p class="text-slate-400 mb-1">
              Size
            </p>

            <p class="font-medium">
              {{ fileSize }}
            </p>

          </div>

        </div>

      </div>

      <!-- Recognition Result -->
      <div
        class="mt-4 bg-slate-900 border border-slate-700 rounded-xl p-4"
      >

        <div class="grid grid-cols-2 gap-4 text-sm">

          <div>

            <p class="text-slate-400 mb-1">
              Model
            </p>

            <p class="font-semibold capitalize">
              {{ selectedModel }}
            </p>

          </div>

          <div>

            <p class="text-slate-400 mb-1">
              Identity
            </p>

            <p class="font-semibold">
              {{ recognitionResult.name }}
            </p>

          </div>

          <div>

            <p class="text-slate-400 mb-1">
              Score
            </p>

            <p class="font-semibold text-emerald-400">
              {{ recognitionResult.score }}
            </p>

          </div>

        </div>

      </div>

      <!-- Action -->
      <button

        @click="processImage"

        :disabled="
          processing ||
          compressing
        "

        class="w-full mt-4 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 disabled:cursor-not-allowed transition-all duration-300 py-3 rounded-xl font-semibold"
      >

        <span v-if="compressing">

          PREPARING IMAGE...

        </span>

        <span v-else-if="processing">

          ANALYZING...

        </span>

        <span v-else>

          START RECOGNITION

        </span>

      </button>

      <button

        @click="clearImage"

        class="w-full mt-3 bg-red-600 hover:bg-red-500 transition-all duration-300 py-3 rounded-xl font-semibold"
      >

        CLEAR IMAGE

      </button>

    </div>

  </div>
</template>

<script setup>
 import { ref } from 'vue'

  import axios from 'axios'

  import imageCompression
  from 'browser-image-compression'


  const fileInput = ref(null)

  const preview = ref(null)

  const previewImage = ref(null)

  const overlayCanvas = ref(null)

  const selectedFile = ref(null)

  const processing = ref(false)

  const compressing = ref(false)

  const bbox = ref(null)

  const fileName = ref('')

  const fileSize = ref('')

  const selectedModel = ref('embedding')

  const recognitionResult = ref({

    name: 'Unknown',

    score: '0.00'
  })

  const analyzedDimensions = ref({

    width: 0,

    height: 0
  })
  function openFile() {

    fileInput.value.click()
  }


  async function handleFile(event) {

    const file = event.target.files[0]

    if (!file) return

    preview.value =
      URL.createObjectURL(file)

    fileName.value = file.name

    compressing.value = true

    bbox.value = null

    try {

      const compressedFile =
        await imageCompression(

          file,

          {

            maxSizeMB: 1,

            maxWidthOrHeight: 1280,

            useWebWorker: true
          }
        )

      selectedFile.value =
        compressedFile

      fileSize.value =
        formatFileSize(
          compressedFile.size
        )

      const bitmap =
        await createImageBitmap(
          compressedFile
        )

      analyzedDimensions.value = {

        width: bitmap.width,

        height: bitmap.height
      }

    } catch (error) {

      console.error(error)

      selectedFile.value = file

    } finally {

      compressing.value = false
    }
  }

  async function processImage() {

    if (!selectedFile.value) return

    processing.value = true

    try {

      const formData = new FormData()

      formData.append(
        'file',
        selectedFile.value
      )

      const response =
        await axios.post(

          `https://aidetection.mektan.my.id/face-api/${
            selectedModel.value === 'embedding'
              ? 'recognize-embedding'
              : 'recognize-classifier'
          }`,

          formData
        )

      const data = response.data

      recognitionResult.value = {

        name: data.name || 'Unknown',

        score: (

          data.similarity ||

          data.confidence ||

          0

        ).toFixed(2)
      }

      bbox.value = data.bbox || null

      setTimeout(
        drawBoundingBox,
        50
      )

    } catch (error) {

      console.error(error)

    } finally {

      processing.value = false
    }
  }


  async function recognizeFace(blob) {

    const formData = new FormData()

    formData.append(
      'file',
      blob,
      'face.jpg'
    )

    const endpoint =

      selectedModel.value === 'embedding'

        ? 'recognize-embedding'

        : 'recognize-classifier'

    const response = await axios.post(

      `https://aidetection.mektan.my.id/face-api/${endpoint}`,

      formData
    )

    const data = response.data

    recognitionResult.value = {

      name: data.name || 'Unknown',

      score: (

        data.similarity ||

        data.confidence ||

        0

      ).toFixed(2)
    }

    bbox.value = data.bbox || null
  }


  function compressImage(file) {

    return new Promise((resolve) => {

      const image = new Image()

      image.onload = () => {

        const canvas =
          document.createElement('canvas')

        const ctx =
          canvas.getContext('2d')

        const maxWidth = 640

        let width = image.width

        let height = image.height

        if (width > maxWidth) {

          const scale =
            maxWidth / width

          width = width * scale

          height = height * scale
        }

        canvas.width = width

        canvas.height = height

        ctx.drawImage(
          image,
          0,
          0,
          width,
          height
        )

        canvas.toBlob(

          blob => {
            resolve(blob)
          },

          'image/jpeg',

          0.6
        )
      }

      image.src =
        URL.createObjectURL(file)
    })
  }

  function drawBoundingBox() {

      if (!bbox.value) return

      const canvas =
        overlayCanvas.value

      const img =
        previewImage.value

      if (!canvas || !img) return

      const ctx =
        canvas.getContext('2d')

      canvas.width =
        img.clientWidth

      canvas.height =
        img.clientHeight

      ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
      )

      const scaleX =

        canvas.width /

        analyzedDimensions.value.width

      const scaleY =

        canvas.height /

        analyzedDimensions.value.height

      const [
        x1,
        y1,
        x2,
        y2
      ] = bbox.value

      const rx = x1 * scaleX

      const ry = y1 * scaleY

      const rw =
        (x2 - x1) * scaleX

      const rh =
        (y2 - y1) * scaleY

      ctx.strokeStyle = '#00ff88'

      ctx.lineWidth = 3

      ctx.strokeRect(
        rx,
        ry,
        rw,
        rh
      )

      const label =
        recognitionResult.value.name

      ctx.font =
        'bold 14px sans-serif'

      const textWidth =
        ctx.measureText(label).width

      ctx.fillStyle =
        '#00ff88'

      ctx.fillRect(
        rx,
        ry - 30,
        textWidth + 20,
        30
      )

      ctx.fillStyle = '#000'

      ctx.fillText(
        label,
        rx + 10,
        ry - 10
      )
    }

    function clearImage() {

        preview.value = null

        selectedFile.value = null

        bbox.value = null

        fileName.value = ''

        fileSize.value = ''

        recognitionResult.value = {

          name: 'Unknown',

          score: '0.00'
        }

        analyzedDimensions.value = {

          width: 0,

          height: 0
        }

        clearCanvas()

        if (fileInput.value) {

          fileInput.value.value = ''
        }
    }

    function clearCanvas() {

    const canvas =
      overlayCanvas.value

    if (!canvas) return

    const ctx =
      canvas.getContext('2d')

    ctx.clearRect(

      0,
      0,

      canvas.width,
      canvas.height
    )
  }

  function formatFileSize(bytes) {

    if (bytes < 1024) {
      return `${bytes} B`
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(2)} KB`
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }
</script>