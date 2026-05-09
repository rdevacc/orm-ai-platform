<template>
  <header
    class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50"
  >

    <div
      class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between"
    >

      <!-- Left -->
      <div>

        <h1
          class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent"
        >
          Face Recognition
        </h1>

        <p class="text-sm text-slate-400 mt-1">
          ArcFace • InsightFace • MobileNetV2
        </p>

      </div>

      <!-- Right -->
      <div class="flex items-center gap-3">

        <div
          class="hidden md:flex items-center gap-2 text-xs bg-emerald-500/10 text-emerald-400 px-3 py-2 rounded-full border border-emerald-500/20"
        >
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          API Online
        </div>

        <a
          href="/"
          class="bg-slate-800 hover:bg-slate-700 transition-all duration-300 px-4 py-2 rounded-xl text-sm border border-slate-700 hover:border-slate-600"
        >
          Kembali
        </a>

      </div>

    </div>

  </header>
</template>

<script setup>
// Minimal header
</script>