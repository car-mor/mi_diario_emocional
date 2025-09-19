<template>
  <BackgroundWrapper>
    <div
      class="max-w-xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors duration-300"
    >
      <h2 class="text-2xl font-semibold mb-6 text-center text-[#70BFE9] dark:text-[#70BFE9]">
        Crear una cuenta para: Profesional de la Salud Mental
      </h2>

      <form v-if="step === 1" @submit.prevent="createInitialAccount">
        <div class="space-y-4">
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Correo electrónico *</label
            >
            <div class="relative flex items-center">
              <IconMail class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.email"
                type="email"
                placeholder="Ingresa tu correo electrónico"
                class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Contraseña *</label
            >
            <div class="relative flex items-center">
              <IconLock class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.password"
                type="password"
                placeholder="Ingresa tu contraseña"
                class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Vuelve a introducir tu contraseña *</label
            >
            <div class="relative flex items-center">
              <IconLock class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.confirmPassword"
                type="password"
                placeholder="Vuelve a introducir la contraseña"
                class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
          </button>
        </div>
      </form>

      <div v-else-if="step === 2" class="text-center">
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Verificación de correo electrónico
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Se envió a tu correo electrónico un código de verificación para comprobar su validez.
        </p>
        <form @submit.prevent="verifyEmail">
          <div class="relative">
            <input
              v-model="form.verificationCode"
              type="text"
              placeholder="Ingresa el código de verificación"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9] text-center"
              required
            />
          </div>
          <p v-if="verificationError" class="text-sm text-red-500 mt-2">
            {{ verificationError }}
          </p>

          <!-- Mostrar tiempo restante para reenvío -->
          <p v-if="isResendDisabled && remainingTime > 0" class="text-sm text-gray-500 mt-2">
            Podrás reenviar el código en {{ Math.ceil(remainingTime / 1000) }} segundos
          </p>

          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            {{ loading ? 'Verificando...' : 'Verificar' }}
          </button>
          <button
            @click.prevent="resendVerificationCode"
            class="w-full mt-4 py-3 px-4 rounded-lg border border-gray-300 dark:border-gray-600 bg-transparent text-gray-800 dark:text-gray-200 font-semibold hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
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
        </form>
      </div>

      <form v-else-if="step === 3" @submit.prevent="submitProfessionalData">
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Nombre(s) *</label
              >
              <input
                v-model="form.name"
                type="text"
                placeholder="Ingresa tu nombre(s)"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Primer apellido *</label
              >
              <input
                v-model="form.paternalLastName"
                type="text"
                placeholder="Ingresa tu primer apellido"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Segundo apellido *</label
              >
              <input
                v-model="form.maternalLastName"
                type="text"
                placeholder="Ingresa tu segundo apellido"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Fecha de nacimiento *</label
              >
              <input
                v-model="form.dateOfBirth"
                type="date"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Sexo *</label
              >
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              >
                <option value="" disabled>Selecciona el sexo...</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
                <option value="non_binary">No binario</option>
                <option value="other">Otro</option>
              </select>
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Cédula profesional *</label
              >
              <input
                v-model="form.professionalLicense"
                type="text"
                placeholder="Ingresa tu No. de Cédula Profesional"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >CURP *</label
              >
              <input
                v-model="form.curp"
                type="text"
                placeholder="Ingresa tu CURP"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Institución de egreso *</label
              >
              <input
                v-model="form.institution"
                type="text"
                placeholder="Ingresa tu Institución de procedencia"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Carrera *</label
            >
            <input
              v-model="form.career"
              type="text"
              placeholder="Ingresa tu carrera o licenciatura"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              required
            />
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            {{ loading ? 'Procesando...' : 'Siguiente' }}
          </button>
        </div>
      </form>

      <div v-else-if="step === 4" class="text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <IconCircleCheckFilled class="text-green-500 w-20 h-20 mb-4" />
          <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">
            ¡Gracias por completar el registro!
          </h3>
          <p class="text-gray-600 dark:text-gray-400 leading-relaxed text-center">
            Te notificaremos cuando se hayan validado tus datos y cédula profesional para que puedas
            comenzar a usar la aplicación. Este proceso puede tardar de 1 a 3 días hábiles.
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
  </BackgroundWrapper>

  <!-- Popup de éxito mejorado -->
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
          {{ successType === 'resend' ? 'Código reenviado' : 'Correo enviado' }}
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

  <!-- Popup de error -->
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
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import BackgroundWrapper from '@/modules/auth/components/BackgroundWrapper.vue'
import { IconMail, IconLock, IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-vue'

const router = useRouter()

const step = ref(1)
const loading = ref(false)
const successPopup = ref(false)
const errorPopup = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const successType = ref('') // 'resend' o 'initial'
const verificationError = ref('')
const lastResendTimestamp = ref(0)
const currentTime = ref(Date.now())
const fiveMinutesInMs = 1 * 60 * 1000

// Intervalo para actualizar el tiempo
let timeInterval: number | null = null

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  verificationCode: '',
  name: '',
  paternalLastName: '',
  maternalLastName: '',
  dateOfBirth: '',
  gender: '',
  professionalLicense: '',
  curp: '',
  institution: '',
  career: '',
})

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

const createInitialAccount = () => {
  if (form.password !== form.confirmPassword) {
    errorMessage.value = 'Las contraseñas no coinciden.'
    errorPopup.value = true
    return
  }

  loading.value = true

  // Simular llamada a API
  setTimeout(() => {
    loading.value = false
    successType.value = 'initial'
    successMessage.value =
      'Se te ha enviado un correo electrónico con un código de verificación para confirmar tu cuenta.'
    successPopup.value = true
    step.value = 2
    lastResendTimestamp.value = Date.now()
  }, 1000)
}

const verifyEmail = () => {
  loading.value = true

  setTimeout(() => {
    if (form.verificationCode === '123456') {
      loading.value = false
      step.value = 3
      verificationError.value = ''
    } else {
      loading.value = false
      verificationError.value = 'Código de verificación incorrecto. Por favor, inténtalo de nuevo.'
    }
  }, 800)
}

const resendVerificationCode = () => {
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
      'Se ha enviado un nuevo código de verificación a tu correo electrónico. Revisa también tu carpeta de spam.'
    successPopup.value = true
    lastResendTimestamp.value = Date.now()

    // Limpiar el código anterior
    form.verificationCode = ''
    verificationError.value = ''

    console.log('Código reenviado exitosamente') // Debug
  }, 1000)
}

const submitProfessionalData = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    step.value = 4
  }, 1000)
}

const goToLogin = () => {
  router.push('/login')
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
</style>
