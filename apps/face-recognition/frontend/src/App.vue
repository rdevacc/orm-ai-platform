<template>
  <div class="min-h-screen bg-slate-900 text-white">

    <TheHeader />

    <main class="max-w-7xl mx-auto px-4 py-10">

      <div class="grid lg:grid-cols-2 gap-8">

        <FaceUpload />

        <LiveRecognition
          @update-result="handleResult"
        />

      </div>

      <ResultPanel

        :embedding-result="embeddingResult"

        :classifier-result="classifierResult"
      />

    </main>

  </div>
</template>

<script setup>

import { ref } from 'vue'

import TheHeader from './components/TheHeader.vue'

import FaceUpload from './components/FaceUpload.vue'

import LiveRecognition from './components/LiveRecognition.vue'

import ResultPanel from './components/ResultPanel.vue'


const embeddingResult = ref({

  name: 'Unknown',

  score: '0.00'
})

const classifierResult = ref({

  name: 'Unknown',

  score: '0.00'
})


function handleResult(payload) {

  const formatted = {

    name: payload.data.name || 'Unknown',

    score: (

      payload.data.similarity ||

      payload.data.confidence ||

      0

    ).toFixed(2)
  }

  if (payload.model === 'embedding') {

    embeddingResult.value = formatted

  } else {

    classifierResult.value = formatted
  }
}
</script>