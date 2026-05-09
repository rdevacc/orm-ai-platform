<template>
  <div
    class="mt-8 bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-xl"
  >

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">

      <div>

        <h2 class="text-xl font-bold">
          Recognition Result
        </h2>

        <p class="text-sm text-slate-400 mt-1">
          Hasil analisa embedding dan classifier neural network
        </p>

      </div>

      <div
        class="flex items-center gap-2 bg-emerald-500/10 text-emerald-400 px-3 py-2 rounded-full border border-emerald-500/20 text-xs"
      >

        <span
          class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"
        ></span>

        Ready

      </div>

    </div>

    <!-- Result Grid -->
    <div class="grid lg:grid-cols-2 gap-6">

      <!-- ===================================================== -->
      <!-- EMBEDDING -->
      <!-- ===================================================== -->

      <div
        class="bg-slate-900 border border-slate-700 rounded-2xl p-6"
      >

        <div class="flex items-center justify-between mb-6">

          <div>

            <h3 class="text-lg font-bold text-emerald-400">
              Embedding Recognition
            </h3>

            <p class="text-xs text-slate-400 mt-1">
              ArcFace + InsightFace
            </p>

          </div>

          <div
            class="bg-emerald-500/10 text-emerald-400 text-xs px-3 py-1 rounded-full"
          >
            ACTIVE
          </div>

        </div>

        <div class="space-y-4 text-sm">

          <!-- Identity -->
          <div
            class="flex items-center justify-between border-b border-slate-800 pb-3"
          >

            <span class="text-slate-400">
              Identity
            </span>

            <span class="font-semibold">
              {{ props.embeddingResult.name }}
            </span>

          </div>

          <!-- Similarity -->
          <div
            class="flex items-center justify-between border-b border-slate-800 pb-3"
          >

            <span class="text-slate-400">
              Similarity
            </span>

            <span class="font-semibold text-emerald-400">
              {{ props.embeddingResult.score }}
            </span>

          </div>

          <!-- Status -->
          <div
            class="flex items-center justify-between"
          >

            <span class="text-slate-400">
              Match Status
            </span>

            <span
              class="bg-red-500/10 text-red-400 text-xs px-3 py-1 rounded-full"
            >
              {{
                props.embeddingResult.name === 'Unknown'
                  ? 'No Match'
                  : 'Matched'
              }}
            </span>

          </div>

        </div>

      </div>


      <!-- ===================================================== -->
      <!-- CLASSIFIER -->
      <!-- ===================================================== -->

      <div
        class="bg-slate-900 border border-slate-700 rounded-2xl p-6"
      >

        <div class="flex items-center justify-between mb-6">

          <div>

            <h3 class="text-lg font-bold text-cyan-400">
              Classifier Recognition
            </h3>

            <p class="text-xs text-slate-400 mt-1">
              MobileNetV2 + Softmax
            </p>

          </div>

          <div
            class="bg-cyan-500/10 text-cyan-400 text-xs px-3 py-1 rounded-full"
          >
            ACTIVE
          </div>

        </div>

        <div class="space-y-4 text-sm">

          <!-- Identity -->
          <div
            class="flex items-center justify-between border-b border-slate-800 pb-3"
          >

            <span class="text-slate-400">
              Identity
            </span>

            <span class="font-semibold">
              {{ props.embeddingResult.name }}
            </span>

          </div>

          <!-- Confidence -->
          <div
            class="flex items-center justify-between border-b border-slate-800 pb-3"
          >

            <span class="text-slate-400">
              Confidence
            </span>

            <span class="font-semibold text-cyan-400">
              {{ props.embeddingResult.score }}
            </span>

          </div>

          <!-- Status -->
          <div
            class="flex items-center justify-between"
          >

            <span class="text-slate-400">
              Prediction Status
            </span>

            <span
              class="bg-red-500/10 text-red-400 text-xs px-3 py-1 rounded-full"
            >
              {{
                props.classifierResult.name === 'Unknown'
                  ? 'No Prediction'
                  : 'Predicted'
              }}
            </span>

          </div>

        </div>

      </div>

    </div>

    <!-- Bottom Info -->
    <div
      class="mt-6 bg-slate-900 border border-slate-700 rounded-2xl p-5"
    >

      <div class="grid md:grid-cols-4 gap-4 text-sm">

        <div>

          <p class="text-slate-400 mb-1">
            Embedding Model
          </p>

          <p class="font-semibold">
            buffalo_s
          </p>

        </div>

        <div>

          <p class="text-slate-400 mb-1">
            Classifier
          </p>

          <p class="font-semibold">
            MobileNetV2
          </p>

        </div>

        <div>

          <p class="text-slate-400 mb-1">
            Backend
          </p>

          <p class="font-semibold text-emerald-400">
            FastAPI
          </p>

        </div>

        <div>

          <p class="text-slate-400 mb-1">
            Runtime
          </p>

          <p class="font-semibold">
            ONNX + TensorFlow
          </p>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

const props = defineProps({

  embeddingResult: {

    type: Object,

    required: true
  },

  classifierResult: {

    type: Object,

    required: true
  }
})
</script>