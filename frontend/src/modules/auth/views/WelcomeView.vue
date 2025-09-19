<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <!-- Grid: 1 columna en móvil, 2 columnas en lg -->
    <div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
      <!-- IZQUIERDA: imagen centrada vertical y horizontalmente -->
      <div class="flex items-center justify-center">
        <WomanHeart />
      </div>

      <!-- DERECHA: tarjeta centrada verticalmente -->
      <div class="flex items-center justify-center p-6">
        <div
          class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-800 p-8 text-center shadow-lg border border-gray-200 dark:border-gray-700"
        >
          <h1 class="mb-4 text-4xl text-brand dark:text-[#70BFE9] font-heading font-semibold">
            ¡Bienvenid@!
          </h1>

          <p class="mb-8 text-gray-600 dark:text-gray-300 leading-relaxed">
            Registra y reflexiona sobre tus emociones cada día.
          </p>

          <div class="flex flex-col items-center gap-4">
            <router-link
              to="/login"
              class="inline-block rounded-lg bg-[#70BFE9] hover:bg-[#5BB1E0] px-6 py-2 font-semibold text-white transition"
            >
              Comenzar
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WomanHeart from '../components/WomanHeart.vue'
</script>
