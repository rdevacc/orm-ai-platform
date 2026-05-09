<template>
  <div class="min-h-screen bg-slate-900 text-white font-sans">

    <!-- Hero Section -->
    <header class="py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">

        <!-- Judul Utama -->
        <h1
          class="text-5xl md:text-6xl font-extrabold mb-6 bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent"
        >
          AI Detection Hub
        </h1>

        <!-- Kalimat Sambutan -->
        <p class="text-lg text-slate-400 mb-10 leading-relaxed">
          Platform terintegrasi untuk pengolahan citra, deteksi objek,
          dan pengenalan wajah berbasis kecerdasan buatan secara real-time.
        </p>

      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-5xl mx-auto px-4 pb-20">

      <div class="grid md:grid-cols-2 gap-8 items-stretch">

        <!-- ===================================================== -->
        <!-- ORM -->
        <!-- ===================================================== -->

        <div
          class="group relative bg-slate-800/50 border border-slate-700 rounded-2xl p-8 hover:border-blue-500 transition-all duration-300 shadow-xl hover:-translate-y-1 h-full flex flex-col"
        >

          <!-- Icon -->
          <div
            class="mb-5 w-12 h-12 bg-blue-500/10 text-blue-500 rounded-xl flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
              />
            </svg>
          </div>

          <!-- Title -->
          <h2 class="text-2xl font-bold mb-3 italic">
            Object Detection (ORM)
          </h2>

          <!-- Desc -->
          <p class="text-slate-400 mb-6 leading-relaxed">
            Analisis objek menggunakan model YOLOv8.
            Mendukung unggah gambar statis dan
            pemindaian langsung melalui kamera perangkat.
          </p>

          <!-- Button -->
          <a
            href="/orm/"
            class="mt-auto inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-300 group-hover:gap-4"
          >
            Buka Aplikasi ORM
            <span>&rarr;</span>
          </a>

        </div>


        <!-- ===================================================== -->
        <!-- FACE RECOGNITION -->
        <!-- ===================================================== -->

        <div
          class="group relative bg-slate-800/50 border border-slate-700 rounded-2xl p-8 hover:border-emerald-500 transition-all duration-300 shadow-xl hover:-translate-y-1 h-full flex flex-col"
        >

          <!-- Icon -->
          <div
            class="mb-5 w-12 h-12 bg-emerald-500/10 text-emerald-400 rounded-xl flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>

          <!-- Title -->
          <h2 class="text-2xl font-bold mb-3 italic">
            Face Recognition
          </h2>

          <!-- Desc -->
          <p class="text-slate-400 mb-6 leading-relaxed">
            Sistem pengenalan wajah berbasis AI menggunakan
            metode embedding dan classifier neural network
            untuk autentikasi biometrik dan identifikasi real-time.
          </p>

          <!-- Badge -->
          <div class="flex flex-wrap gap-2 mb-6">

            <span
              class="text-xs bg-slate-700 text-slate-300 px-3 py-1 rounded-full"
            >
              ArcFace
            </span>

            <span
              class="text-xs bg-slate-700 text-slate-300 px-3 py-1 rounded-full"
            >
              InsightFace
            </span>

            <span
              class="text-xs bg-slate-700 text-slate-300 px-3 py-1 rounded-full"
            >
              MobileNetV2
            </span>

          </div>

          <!-- Button -->
          <a
            href="/face/"
            class="mt-auto inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-300 group-hover:gap-4"
          >
            Buka Face Recognition
            <span>&rarr;</span>
          </a>

        </div>

      </div>

    </main>

    <!-- Footer -->
    <footer
      class="border-t border-slate-800 py-10 text-center text-slate-500 text-sm"
    >
      <p>&copy; 2026 AI Detection Portal</p>
    </footer>

  </div>
</template>

<script setup>
// Minimalis tanpa logic berat
</script>

<style>
/* Tailwind v4 support */
</style>