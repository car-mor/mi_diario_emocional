<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
      <div class="flex items-center justify-center">
        <WomanHeart />
      </div>

      <div class="flex items-center justify-center p-6">
        <div
          class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-800 p-8 shadow-lg border border-gray-200 dark:border-gray-700"
        >
          <h1 class="mb-8 text-3xl font-bold text-center text-[#70BFE9]">Regístrate</h1>

          <div class="flex flex-col gap-6 text-center">
            <div>
              <p class="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-200">
                ¿Eres un profesional de la salud mental?
              </p>
              <router-link
                to="/privacy-policy?flow=register&type=professional"
                class="inline-block w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                ¡Haz click aquí!
              </router-link>
            </div>

            <div>
              <p class="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-200">
                ¿Eres un paciente?
              </p>
              <router-link
                to="/privacy-policy?flow=register&type=patient"
                class="inline-block w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                ¡Haz click aquí!
              </router-link>
            </div>
          </div>

          <div class="mt-8">
            <router-link
              to="/"
              class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Regresar al Inicio
            </router-link>
          </div>

          <div class="mt-8 text-center text-gray-600 dark:text-gray-400">
            ¿Ya tienes una cuenta?
            <router-link to="/login" class="text-[#70BFE9] hover:underline font-semibold ml-1">
              Inicia sesión aquí
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WomanHeart from '../components/WomanHeart.vue'

// No se necesita lógica JS en este componente, ya que los links de Vue Router manejan la navegación.
</script>
