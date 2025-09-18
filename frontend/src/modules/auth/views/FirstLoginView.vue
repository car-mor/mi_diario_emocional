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
          <h1 class="mb-8 text-2xl font-bold text-center text-[#70BFE9]">
            Inicia sesión por primera vez como Paciente
          </h1>

          <form @submit.prevent="firstTimeLogin">
            <div class="mb-6">
              <label
                for="email"
                class="block text-gray-700 dark:text-gray-300 text-base font-semibold mb-2"
              >
                Correo electrónico
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <IconMail class="h-6 w-6 mx-auto text-[#70BFE9] dark:text-gray-300" />
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

            <div class="mb-6">
              <label
                for="password"
                class="block text-gray-700 dark:text-gray-300 text-base font-semibold mb-2"
              >
                Contraseña
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <IconLockSquareRounded
                    class="h-6 w-6 mx-auto text-[#70BFE9] dark:text-gray-300"
                  />
                </div>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  placeholder="Ingresa tu contraseña"
                  class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
                  required
                />
              </div>
            </div>

            <div class="mb-6">
              <label
                for="validationCode"
                class="block text-gray-700 dark:text-gray-300 text-base font-semibold mb-2"
              >
                Código de validación enviado a tu correo
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <IconAlertCircle class="h-6 w-6 mx-auto text-yellow-500 dark:text-yellow-400" />
                </div>
                <input
                  type="text"
                  id="validationCode"
                  v-model="validationCode"
                  placeholder="Ingresa tu código..."
                  class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              class="w-full bg-[#70BFE9] hover:bg-[#5a9cbf] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
            >
              Iniciar sesión
            </button>
            <button
              @click.prevent="resendCode"
              class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Volver a enviar código
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-if="errorPopup" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center">
      <div class="flex flex-col items-center justify-center">
        <IconCircleXFilled class="text-red-500 w-16 h-16 mb-4" />
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">Error</h3>
        <p class="text-gray-600 dark:text-gray-300 mb-4">{{ errorMessage }}</p>
        <button
          @click="closeErrorPopup"
          class="bg-red-500 text-white font-semibold py-2 px-6 rounded-lg hover:bg-red-600 transition-colors"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>

  <div v-if="resendPopup" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center">
      <div class="flex flex-col items-center justify-center">
        <IconCircleCheckFilled class="text-green-500 w-16 h-16 mb-4" />
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">Código enviado</h3>
        <p class="text-gray-600 dark:text-gray-300 mb-4">
          Se ha enviado un nuevo código de validación a tu correo. Por favor, revisa tu bandeja de
          entrada. Puedes reenviar un nuevo código en 5 minutos.
        </p>
        <button
          @click="closeResendPopup"
          class="bg-green-500 text-white font-semibold py-2 px-6 rounded-lg hover:bg-green-600 transition-colors"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  IconLockSquareRounded,
  IconMail,
  IconAlertCircle,
  IconCircleXFilled,
  IconCircleCheckFilled,
} from '@tabler/icons-vue'
import WomanHeart from '../components/WomanHeart.vue'

const email = ref('')
const password = ref('')
const validationCode = ref('')
const errorPopup = ref(false)
const resendPopup = ref(false)
const errorMessage = ref('')
const lastResendTimestamp = ref(0)

const isEmailValid = (email: string): boolean => {
  const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
  return re.test(String(email).toLowerCase())
}

const firstTimeLogin = () => {
  if (!isEmailValid(email.value)) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico con un formato válido.'
    errorPopup.value = true
    return
  }

  // Lógica de autenticación
  console.log('Intento de inicio de sesión por primera vez con:', {
    email: email.value,
    password: password.value,
    validationCode: validationCode.value,
  })

  // Simulación de respuesta de API:
  const isLoginSuccessful =
    email.value === 'test@example.com' &&
    password.value === 'password123' &&
    validationCode.value === '123456'

  if (!isLoginSuccessful) {
    errorMessage.value =
      'Las credenciales no son correctas. Por favor, verifica tu correo, contraseña o el código de validación.'
    errorPopup.value = true
  } else {
    // Si la autenticación es exitosa, redirige al usuario
    console.log('Inicio de sesión exitoso. Redirigiendo...')
    // router.push('/dashboard');
  }
}

const resendCode = () => {
  const currentTime = Date.now()
  const fiveMinutesInMs = 5 * 60 * 1000

  if (currentTime - lastResendTimestamp.value < fiveMinutesInMs) {
    errorMessage.value = 'Debes esperar 5 minutos antes de volver a enviar el código.'
    errorPopup.value = true
    return
  }

  // Lógica para reenviar el código de validación
  console.log('Solicitud para reenviar código a:', email.value)
  // Aquí llamarías a una API para reenviar el código

  // Simulación de respuesta exitosa de API
  resendPopup.value = true
  lastResendTimestamp.value = currentTime
}

const closeErrorPopup = () => {
  errorPopup.value = false
  errorMessage.value = ''
}

const closeResendPopup = () => {
  resendPopup.value = false
}
</script>
