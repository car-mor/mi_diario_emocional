<template>
  <div
    class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-800 p-2 shadow-lg border border-gray-200 dark:border-gray-700"
  >
    <h1 class="mb-4 text-3xl font-bold text-center text-[#70BFE9] dark:text-gray-200">
      Recuperar contraseña
    </h1>

    <div v-if="currentStep === 1" class="text-center">
      <p class="mb-6 text-gray-600 dark:text-gray-400 leading-relaxed">
        Ingresa el correo electrónico del cual quieres recuperar su contraseña
      </p>
      <div class="mb-6">
        <label for="email" class="sr-only">Correo electrónico</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <svg
              class="w-5 h-5 text-gray-400 dark:text-gray-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8m-17 0V6a2 2 0 012-2h14a2 2 0 012 2v2m-18 0a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-18 0h18"
              />
            </svg>
          </div>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Ingresa tu correo electrónico"
            class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
            required
          />
        </div>
      </div>
      <button
        @click="goToStep(2)"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
      >
        Enviar código de verificación
      </button>
      <button
        @click="goToStep(0)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Cancelar
      </button>
    </div>

    <div v-else-if="currentStep === 2" class="text-center">
      <p class="mb-6 text-gray-600 dark:text-gray-400 leading-relaxed">
        Se envió a tu correo electrónico un código de confirmación para la recuperación de la
        contraseña. Este código expirará una vez transcurridos 5 minutos.
      </p>
      <div class="mb-6">
        <label for="code" class="sr-only">Código de verificación</label>
        <input
          type="text"
          id="code"
          v-model="code"
          placeholder="Código de verificación"
          class="p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
          required
        />
      </div>
      <button
        @click="goToStep(3)"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
      >
        Recuperar contraseña
      </button>
      <button
        @click="goToStep(1)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
      >
        Volver a enviar código
      </button>
      <button
        @click="goToStep(0)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Cancelar
      </button>
    </div>

    <div v-else-if="currentStep === 3" class="text-center">
      <p class="mb-6 text-gray-600 dark:text-gray-400 leading-relaxed">
        Por favor, escribe tu nueva contraseña a utilizar
      </p>
      <div class="mb-4">
        <label for="new-password" class="sr-only">Nueva contraseña</label>
        <input
          type="password"
          id="new-password"
          v-model="newPassword"
          placeholder="Nueva contraseña"
          class="p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
          required
        />
      </div>
      <div class="mb-6">
        <label for="confirm-password" class="sr-only">Confirmación de contraseña</label>
        <input
          type="password"
          id="confirm-password"
          v-model="confirmPassword"
          placeholder="Confirmación de contraseña"
          class="p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
          required
        />
      </div>
      <button
        @click="goToStep(0)"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
      >
        Confirmar nueva contraseña
      </button>
      <button
        @click="goToStep(0)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Cancelar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentStep = ref<number>(1)
const email = ref<string>('')
const code = ref<string>('')
const newPassword = ref<string>('')
const confirmPassword = ref<string>('')

const goToStep = (step: number) => {
  currentStep.value = step
  // En una implementación real, aquí se llamaría a la API
  // y solo se cambiaría de paso si la respuesta es exitosa.
}
</script>
