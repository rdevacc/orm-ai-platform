<template>
  <div
    class="bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-xl h-full flex flex-col"
  >

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">

      <div class="flex items-center gap-3">

        <div
          class="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center"
        >
          🎥
        </div>

        <div>

          <h2 class="text-xl font-bold">
            Live Recognition
          </h2>

          <p class="text-sm text-slate-400 mt-1">
            Realtime webcam face recognition
          </p>

        </div>

      </div>

      <div class="mb-6">
        <!-- MODEL SELECT -->
        <label
            class="block text-sm text-slate-400 mb-2"
          >
            Recognition Model
          </label>
          
        <select
          v-model="selectedModel"
          class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-cyan-500"
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

    <!-- Camera Area -->
    <div
      class="relative aspect-video rounded-2xl overflow-hidden border border-slate-700 bg-black flex items-center justify-center"
    >

      <!-- Video -->
      <video
        ref="video"
        autoplay
        playsinline
        muted
        class="w-full h-full object-cover"
      />

      <!-- Canvas Overlay -->
      <canvas
        ref="overlay"
        class="absolute inset-0 w-full h-full pointer-events-none"
      ></canvas>

      <!-- Overlay -->
      <div
        v-if="!cameraActive"
        class="absolute inset-0 flex flex-col items-center justify-center bg-black/60"
      >

        <div
          class="w-20 h-20 rounded-2xl bg-slate-800 flex items-center justify-center text-4xl mb-4 border border-slate-700"
        >
          📹
        </div>

        <h3 class="text-lg font-semibold mb-2">
          Kamera Belum Aktif
        </h3>

        <p class="text-slate-400 text-sm">
          Tekan tombol Start Camera
        </p>

      </div>

      <!-- Status -->
      <div
        v-if="detecting"
        class="absolute top-4 left-4 flex items-center gap-2 bg-black/60 backdrop-blur px-3 py-2 rounded-full border border-slate-700"
      >

        <span
          class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"
        ></span>

        <span class="text-xs text-white">
          SYSTEM ACTIVE
        </span>

      </div>

    </div>

    <!-- Controls -->
    <div class="grid grid-cols-2 gap-4 mt-6">

      <button
        @click="toggleRecognition"
        :disabled="!cameraActive"
        class="bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 disabled:cursor-not-allowed transition-all duration-300 py-3 rounded-xl font-semibold"
      >
        {{
          detecting
            ? 'Stop Recognition'
            : 'Start Recognition'
        }}
      </button>

      <button
        @click="stopCamera"
        class="bg-red-600 hover:bg-red-500 transition-all duration-300 py-3 rounded-xl font-semibold"
      >
        Stop Camera
      </button>

    </div>

    <!-- Info -->
    <div
      class="mt-6 bg-slate-900 border border-slate-700 rounded-xl p-4"
    >

      <div class="grid grid-cols-2 gap-4 text-sm">

        <div>

          <p class="text-slate-400 mb-1">
            Status
          </p>

          <p
            :class="
              cameraActive
                ? 'text-emerald-400'
                : 'text-red-400'
            "
            class="font-semibold"
          >
            {{
              cameraActive
                ? 'Active'
                : 'Inactive'
            }}
          </p>

        </div>

        <div>

          <p class="text-slate-400 mb-1">
            Model
          </p>

          <p class="font-semibold text-cyan-400">
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

    <!-- Hidden Canvas -->
    <canvas
      ref="captureCanvas"
      width="640"
      height="480"
      class="hidden"
    ></canvas>

  </div>
</template>

<script setup>
  import { ref, onMounted, onUnmounted } from 'vue'

  import axios from 'axios'


  const emit = defineEmits([
    'update-result'
  ])


  let isProcessing = false

  const video = ref(null)

  const overlay = ref(null)

  const captureCanvas = ref(null)

  const cameraActive = ref(false)

  const detecting = ref(false)

  const selectedModel = ref('embedding')

  const recognitionResult = ref({

    name: 'Unknown',

    score: '0.00'
  })

  const faces = ref([])

  let stream = null


  async function startCamera() {

    try {

      stream = await navigator.mediaDevices.getUserMedia({
        video: true
      })

      video.value.srcObject = stream

      cameraActive.value = true

    } catch (error) {

      console.error(error)

      alert('Tidak dapat mengakses kamera')
    }
  }


  function stopCamera() {

    detecting.value = false

    if (!stream) return

    clearOverlay()

    stream.getTracks().forEach(track => {
      track.stop()
    })

    video.value.srcObject = null

    cameraActive.value = false
  }


  function toggleRecognition() {

    detecting.value = !detecting.value

    if (detecting.value) {

      runRecognition()

    } else {

      clearOverlay()
    }
  }


  async function runRecognition() {

    if (!detecting.value) return

    if (isProcessing) {

      setTimeout(
        runRecognition,
        700
      )

      return
    }

    isProcessing = true

    const ctx =
      captureCanvas.value.getContext('2d')

    ctx.drawImage(

      video.value,

      0,
      0,

      480,
      360
    )

    captureCanvas.value.toBlob(

      async blob => {

        const formData = new FormData()

        formData.append(
          'file',
          blob,
          'frame.jpg'
        )

        try {

          const endpoint =

            selectedModel.value === 'embedding'

              ? 'recognize-embedding'

              : 'recognize-classifier'

          const response = await axios.post(

            `https://aidetection.mektan.my.id/face-api/${endpoint}`,

            formData
          )

          const data = response.data

          console.log(data)

          faces.value = data.faces || []

          if (faces.value.length > 0) {

            const firstFace =
              faces.value[0]

            recognitionResult.value = {

              name:
                firstFace.name ||

                'Unknown',

              score: (

                firstFace.similarity ||

                firstFace.confidence ||

                0

              ).toFixed(2)
            }

          } else {

            recognitionResult.value = {

              name: 'Unknown',

              score: '0.00'
            }
          }

          emit(

            'update-result',

            {

              model: selectedModel.value,

              data
            }
          )

          drawBoundingBoxes(faces.value)

        } catch (error) {

          console.error(error)

        } finally {

          isProcessing = false

          setTimeout(
            runRecognition,
            700
          )
        }
      },

      'image/jpeg',

      0.6
    )
  }


  function drawBoundingBoxes(faces) {

    const canvas = overlay.value

    const videoEl = video.value

    if (!canvas || !videoEl) return

    const ctx = canvas.getContext('2d')

    canvas.width =
      videoEl.clientWidth

    canvas.height =
      videoEl.clientHeight

    ctx.clearRect(

      0,
      0,

      canvas.width,
      canvas.height
    )

    const scaleX =
      canvas.width / 480

    const scaleY =
      canvas.height / 360

    faces.forEach(face => {

      if (!face.bbox) return

      const [
        x1,
        y1,
        x2,
        y2
      ] = face.bbox

      const rectX = x1 * scaleX

      const rectY = y1 * scaleY

      const rectW =
        (x2 - x1) * scaleX

      const rectH =
        (y2 - y1) * scaleY

      ctx.strokeStyle =

        face.name === 'Unknown'

          ? '#ff4444'

          : '#00ff88'

      ctx.lineWidth = 3

      ctx.strokeRect(

        rectX,
        rectY,

        rectW,
        rectH
      )

      const label =
        `${face.name}`

      ctx.font =
        'bold 14px sans-serif'

      const textWidth =
        ctx.measureText(label).width

      ctx.fillStyle =

        face.name === 'Unknown'

          ? '#ff4444'

          : '#00ff88'

      ctx.fillRect(

        rectX,
        rectY - 30,

        textWidth + 20,
        30
      )

      ctx.fillStyle = '#000'

      ctx.fillText(

        label,

        rectX + 10,
        rectY - 10
      )
    })
  }


  function clearOverlay() {

    const canvas = overlay.value

    if (!canvas) return

    const ctx = canvas.getContext('2d')

    ctx.clearRect(

      0,
      0,

      canvas.width,
      canvas.height
    )

    canvas.width = canvas.width
  }


  onMounted(() => {

    startCamera()
  })


  onUnmounted(() => {

    stopCamera()
  })
</script>