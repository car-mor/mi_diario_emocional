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
            <IconMail class="h-6 w-6 mx-auto text-[#70BFE9] dark:text-gray-300" />
          </div>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Ingresa tu correo electrónico"
            class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
            required
            :disabled="loading"
          />
        </div>
      </div>
      <button
        @click="sendRecoveryCode"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading || !email"
      >
        {{ loading ? 'Enviando...' : 'Enviar código de verificación' }}
      </button>
      <button
        @click="goToLogin"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
        :disabled="loading"
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
          :disabled="loading"
        />
      </div>

      <p v-if="codeError" class="text-sm text-red-500 mb-4">
        {{ codeError }}
      </p>

      <p v-if="isResendDisabled && remainingTime > 0" class="text-sm text-gray-500 mb-4">
        Podrás reenviar el código en {{ Math.ceil(remainingTime / 1000) }} segundos
      </p>

      <button
        @click="verifyCode"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading || !code"
      >
        {{ loading ? 'Verificando...' : 'Recuperar contraseña' }}
      </button>

      <button
        @click="resendRecoveryCode"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading || isResendDisabled"
      >
        {{
          loading
            ? 'Enviando...'
            : isResendDisabled
              ? `Esperar ${Math.ceil(remainingTime / 1000)}s`
              : 'Volver a enviar código'
        }}
      </button>

      <button
        @click="goToStep(0)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
        :disabled="loading"
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
          :disabled="loading"
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
          :disabled="loading"
        />
      </div>

      <p v-if="passwordError" class="text-sm text-red-500 mb-4">
        {{ passwordError }}
      </p>

      <button
        @click="confirmNewPassword"
        class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading || !newPassword || !confirmPassword"
      >
        {{ loading ? 'Procesando...' : 'Confirmar nueva contraseña' }}
      </button>

      <button
        @click="goToStep(0)"
        class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
        :disabled="loading"
      >
        Cancelar
      </button>
    </div>

    <div v-else-if="currentStep === 4" class="text-center">
      <div class="flex flex-col items-center justify-center space-y-4">
        <IconCircleCheckFilled class="text-green-500 w-20 h-20 mb-4" />
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">
          ¡Contraseña actualizada!
        </h3>
        <p class="text-gray-600 dark:text-gray-400 leading-relaxed text-center">
          Tu contraseña ha sido actualizada exitosamente. Ya puedes iniciar sesión con tu nueva
          contraseña.
        </p>
      </div>
      <button
        @click="goToLogin"
        class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
      >
        Ir a inicio de sesión
      </button>
    </div>
  </div>

  <div
    v-if="successPopup"
    class="fixed inset-0 flex items-center justify-center z-50"
    @click="closeSuccessPopup"
  >
    <div
      class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center m-4"
      @click.stop
    >
      <div class="flex flex-col items-center justify-center">
        <IconCircleCheckFilled class="text-green-500 w-16 h-16 mb-4" />
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">
          {{ successType === 'resend' ? 'Código reenviado' : 'Código enviado' }}
        </h3>
        <p class="text-gray-600 dark:text-gray-300 mb-4">{{ successMessage }}</p>
        <button
          @click="closeSuccessPopup"
          class="bg-green-500 text-white font-semibold py-2 px-6 rounded-lg hover:bg-green-600 transition-colors"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>

  <div
    v-if="errorPopup"
    class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50"
    @click="closeErrorPopup"
  >
    <div
      class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center m-4"
      @click.stop
    >
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { IconMail, IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-vue'

const router = useRouter() // Inicializa el router

const currentStep = ref<number>(1)
const loading = ref(false)
const email = ref<string>('')
const code = ref<string>('')
const newPassword = ref<string>('')
const confirmPassword = ref<string>('')

// Estados para popups
const successPopup = ref(false)
const errorPopup = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const successType = ref('') // 'resend' o 'initial'

// Estados para validación
const codeError = ref('')
const passwordError = ref('')

// Control de tiempo para reenvío
const lastResendTimestamp = ref(0)
const currentTime = ref(Date.now())
const fiveMinutesInMs = 1 * 60 * 1000

// Intervalo para actualizar el tiempo
let timeInterval: number | null = null

const remainingTime = computed(() => {
  if (lastResendTimestamp.value === 0) return 0
  const elapsed = currentTime.value - lastResendTimestamp.value
  return Math.max(0, fiveMinutesInMs - elapsed)
})

const isResendDisabled = computed(() => {
  return remainingTime.value > 0
})

// Iniciar el contador de tiempo
const startTimer = () => {
  if (timeInterval) clearInterval(timeInterval)
  timeInterval = setInterval(() => {
    currentTime.value = Date.now()
  }, 1000)
}

// Limpiar el contador
const stopTimer = () => {
  if (timeInterval) {
    clearInterval(timeInterval)
    timeInterval = null
  }
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  stopTimer()
})

const goToStep = (step: number) => {
  if (step === 0) {
    // Si se hace clic en Cancelar, volvemos al paso 1 y limpiamos el formulario
    currentStep.value = 1
    email.value = ''
    code.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } else {
    currentStep.value = step
  }
  // Limpiar errores al cambiar de paso
  codeError.value = ''
  passwordError.value = ''
}

// Función para redireccionar a la página de login
const goToLogin = () => {
  router.push('/login')
}

const sendRecoveryCode = () => {
  if (!email.value) {
    errorMessage.value = 'Por favor, ingresa tu correo electrónico.'
    errorPopup.value = true
    return
  }

  loading.value = true

  // Simular llamada a API
  setTimeout(() => {
    loading.value = false
    successType.value = 'initial'
    successMessage.value =
      'Se ha enviado un código de recuperación a tu correo electrónico. Revisa también tu carpeta de spam.'
    successPopup.value = true
    currentStep.value = 2
    lastResendTimestamp.value = Date.now()

    console.log('Código de recuperación enviado') // Debug
  }, 1000)
}

const verifyCode = () => {
  if (!code.value) {
    codeError.value = 'Por favor, ingresa el código de verificación.'
    return
  }

  loading.value = true

  // Simular verificación de código (código correcto: '123456')
  setTimeout(() => {
    loading.value = false
    if (code.value === '123456') {
      currentStep.value = 3
      codeError.value = ''
    } else {
      codeError.value = 'Código de verificación incorrecto. Por favor, inténtalo de nuevo.'
    }
  }, 800)
}

const resendRecoveryCode = () => {
  if (isResendDisabled.value) {
    errorMessage.value = `Debes esperar ${Math.ceil(remainingTime.value / 1000)} segundos antes de volver a solicitar un código.`
    errorPopup.value = true
    return
  }

  loading.value = true

  // Simular llamada a API para reenvío
  setTimeout(() => {
    loading.value = false
    successType.value = 'resend'
    successMessage.value =
      'Se ha enviado un nuevo código de recuperación a tu correo electrónico. Revisa también tu carpeta de spam.'
    successPopup.value = true
    lastResendTimestamp.value = Date.now()

    // Limpiar el código anterior y errores
    code.value = ''
    codeError.value = ''

    console.log('Código de recuperación reenviado exitosamente') // Debug
  }, 1000)
}

const confirmNewPassword = () => {
  if (!newPassword.value || !confirmPassword.value) {
    passwordError.value = 'Por favor, completa ambos campos de contraseña.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'Las contraseñas no coinciden.'
    return
  }

  if (newPassword.value.length < 8) {
    passwordError.value = 'La contraseña debe tener al menos 8 caracteres.'
    return
  }

  loading.value = true

  // Simular actualización de contraseña
  setTimeout(() => {
    loading.value = false
    passwordError.value = ''
    currentStep.value = 4

    console.log('Contraseña actualizada exitosamente') // Debug
  }, 1000)
}

const closeSuccessPopup = () => {
  successPopup.value = false
  successType.value = ''
  successMessage.value = ''
}

const closeErrorPopup = () => {
  errorPopup.value = false
  errorMessage.value = ''
}
</script>

<style scoped>
/* Animaciones para los popups */
.fixed {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Transiciones suaves para los pasos */
div[class*='text-center'] {
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
