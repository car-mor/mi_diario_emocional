<template>
  <BackgroundWrapper>
    <div
      class="max-w-5xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors duration-300"
    >
      <h2 class="text-2xl font-semibold mb-6 text-center text-[#70BFE9] dark:text-[#70BFE9]">
        Crear una cuenta para: Paciente
      </h2>

      <form v-if="step === 1" @submit.prevent="verifyLinkCode">
        <div class="flex flex-col items-center justify-center space-y-4">
          <p class="text-gray-600 dark:text-gray-300 text-center mb-4">
            Código de enlace proporcionado por tu profesional de la Salud Mental
          </p>
          <div class="relative w-full">
            <input
              v-model="linkCode"
              type="text"
              placeholder="Ingresa tu código..."
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLink
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
            />
          </div>
          <p v-if="error" class="text-sm text-red-500 mt-2">{{ error }}</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Siguiente
          </button>
        </div>
      </form>

      <form v-else-if="step === 2" @submit.prevent="submitPersonalData">
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <input
                v-model="form.name"
                type="text"
                placeholder="Ingresa tu nombre(s)"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconUser
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
            <div class="relative">
              <input
                v-model="form.alias"
                type="text"
                placeholder="Ingresa tu alias..."
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconUserPlus
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <input
                v-model="form.paternalLastName"
                type="text"
                placeholder="Ingresa tu primer apellido"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconUserCheck
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
            <div class="relative">
              <input
                v-model="form.maternalLastName"
                type="text"
                placeholder="Ingresa tu segundo apellido"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconUserCheck
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <input
                v-model="form.dateOfBirth"
                type="date"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconCalendar
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
            <div class="relative">
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              >
                <option value="" disabled>Selecciona el género...</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
                <option value="non_binary">No binario</option>
                <option value="other">Otro</option>
              </select>
              <IconGenderBigender
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Siguiente
          </button>
        </div>
      </form>

      <form v-else-if="step === 3" @submit.prevent="createAccount">
        <div class="space-y-4">
          <div class="relative">
            <input
              v-model="form.email"
              type="email"
              placeholder="Ingresa tu correo electrónico"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              required
              :style="{ 'padding-left': '3rem' }"
            />
            <IconMail
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
            />
          </div>
          <div class="relative">
            <input
              v-model="form.password"
              type="password"
              placeholder="Ingresa tu contraseña"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              required
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLock
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
            />
          </div>
          <div class="relative">
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="Vuelve a introducir la contraseña"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              required
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLock
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
            />
          </div>
          <p v-if="passwordError" class="text-sm text-red-500 mt-2">{{ passwordError }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Crear cuenta
          </button>
        </div>
      </form>

      <div v-else-if="step === 4" class="text-center">
        <div class="mb-6 flex flex-col items-center">
          <IconCircleCheckFilled class="text-green-500 w-20 h-20 mb-4" />
          <p class="text-lg font-medium text-gray-700 dark:text-gray-200">
            ¡Gracias por completar el registro!
          </p>
        </div>
        <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">
          Se te ha enviado un correo electrónico con un código de validación para confirmar tu
          cuenta.
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Revisa tu bandeja de entrada y, si no lo encuentras, revisa también la carpeta de spam.
        </p>
        <button
          @click="goToLogin"
          class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
        >
          Iniciar sesión
        </button>
      </div>
    </div>
  </BackgroundWrapper>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import BackgroundWrapper from '@/modules/auth/components/BackgroundWrapper.vue'
import {
  IconLink,
  IconUser,
  IconUserPlus,
  IconUserCheck,
  IconCalendar,
  IconGenderBigender,
  IconMail,
  IconLock,
  IconCircleCheckFilled,
} from '@tabler/icons-vue'

const router = useRouter()

const step = ref(1)
const linkCode = ref('')
const professionalId = ref('')
const error = ref('')
const passwordError = ref('')
const loading = ref(false)

const form = reactive({
  name: '',
  alias: '',
  paternalLastName: '',
  maternalLastName: '',
  dateOfBirth: '',
  gender: '',
  email: '',
  password: '',
  confirmPassword: '',
})

async function verifyLinkCode() {
  loading.value = true
  error.value = ''
  try {
    // Aquí iría la llamada a tu API de Django para validar el código
    // const response = await api.post('/api/validate-link-code/', { link_code: linkCode.value });
    // if (response.data.professional_id) {
    //   professionalId.value = response.data.professional_id;
    //   step.value = 2; // Avanzar al siguiente paso
    // } else {
    //   error.value = 'Código de enlace inválido. Por favor, verifica el código e inténtalo de nuevo.';
    // }

    // Simulación de respuesta exitosa
    if (linkCode.value === '123456') {
      professionalId.value = 'prof-uuid-123'
      step.value = 2
    } else {
      error.value = 'Código de enlace inválido. Por favor, verifica el código e inténtalo de nuevo.'
    }
  } catch (err: unknown) {
    // Ahora 'err' es de tipo 'unknown', más seguro que 'any'.
    // Debes verificar su tipo antes de usarlo.
    if (err instanceof Error) {
      error.value = err.message
    } else {
      error.value = 'Ocurrió un error. Por favor, inténtalo de nuevo.'
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

function submitPersonalData() {
  // Lógica de validación básica de los campos personales
  if (
    form.name &&
    form.alias &&
    form.paternalLastName &&
    form.maternalLastName &&
    form.dateOfBirth &&
    form.gender
  ) {
    step.value = 3 // Avanzar al siguiente paso
  } else {
    // Manejar error de campos incompletos
  }
}

async function createAccount() {
  if (form.password !== form.confirmPassword) {
    passwordError.value = 'Las contraseñas no coinciden.'
    return
  }

  loading.value = true
  passwordError.value = ''

  try {
    const registrationData = {
      ...form,
      professional_id: professionalId.value,
    }

    // Aquí iría la llamada a tu API de Django para registrar al usuario
    // Esta línea se descomentará cuando la API esté lista.
    // const response = await api.post('/api/register-patient/', registrationData);
    // console.log(response.data); // Usar la variable para evitar el error de linter

    console.log(registrationData) // Se usa la variable para evitar el error de linter

    step.value = 4 // Mostrar el mensaje de éxito
  } catch (err: unknown) {
    // Ahora 'err' es de tipo 'unknown', más seguro que 'any'.
    // Debes verificar su tipo antes de usarlo.
    if (err instanceof Error) {
      passwordError.value = err.message
    } else {
      passwordError.value = 'Ocurrió un error al crear la cuenta. Por favor, inténtalo de nuevo.'
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push('/first-login')
}
</script>
