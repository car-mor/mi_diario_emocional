<template>
  <BackgroundWrapper>
    <div
      class="max-w-xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors duration-300"
    >
      <h2 class="text-2xl font-semibold mb-6 text-center text-[#70BFE9] dark:text-[#70BFE9]">
        Crear una cuenta para: Profesional de la Salud Mental
      </h2>

      <form v-if="step === 1" @submit.prevent="submitRegistration">
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
           <p v-if="passwordError" class="text-sm text-red-500 mt-2">{{ passwordError }}</p>

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

          <p class="text-sm text-gray-500 dark:text-gray-400 pt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            {{ loading ? 'Enviando solicitud...' : 'Enviar para Revisión' }}
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
            Te notificaremos por correo cuando hayamos validado tus datos y cédula profesional para que puedas
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

  <div
    v-if="errorPopup"
    class="fixed inset-0 flex items-center justify-center z-50"
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { isAxiosError } from 'axios';
import * as AuthServices from '@/modules/auth/services/authServices';
import BackgroundWrapper from '@/modules/auth/components/BackgroundWrapper.vue'
import { IconMail, IconLock, IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-vue'

const router = useRouter()

const step = ref(1) // 1 para el formulario, 4 para el mensaje de éxito
const loading = ref(false)
const errorPopup = ref(false)
const errorMessage = ref('')
const passwordError = ref(''); // Para el error de contraseñas que no coinciden

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  name: '',
  paternalLastName: '',
  maternalLastName: '',
  dateOfBirth: '',
  gender: '', // 'sex' en el backend
  professionalLicense: '',
  curp: '',
  institution: '',
  career: '',
})

// Función única para enviar todo el formulario
const submitRegistration = async () => {
  // 1. Validación de contraseña en el frontend
  if (form.password !== form.confirmPassword) {
    passwordError.value = 'Las contraseñas no coinciden.';
    return;
  }
  passwordError.value = '';
  loading.value = true;

  // 2. Construir el payload EXACTAMENTE como lo espera tu ProfessionalSerializer
  const registrationPayload = {
      user: {
          email: form.email,
          password: form.password,
          name: form.name,
          paternal_last_name: form.paternalLastName,
          maternal_last_name: form.maternalLastName,
          date_of_birth: form.dateOfBirth,
          role: "professional"
      },
      sex: form.gender,
      professional_license: form.professionalLicense,
      curp: form.curp,
      institution: form.institution,
      career: form.career,
      // El link_code se genera en el backend, no es necesario enviarlo
  };

  try {
    const response = await AuthServices.registerProfessional(registrationPayload);
    if (response.status === 201) {
        // Éxito: El profesional está pre-registrado y pendiente de revisión.
        step.value = 4; // Avanza a la pantalla de "Gracias, estamos revisando"
    }
  } catch (error: unknown) {
    if (isAxiosError(error) && error.response) {
      const data = error.response.data;
      let msg = 'Error de registro. Verifique sus datos.';

      // Manejo de errores anidados
      if (data.user && data.user.email) msg = `Email: ${data.user.email[0]}`;
      else if (data.professional_license) msg = `Cédula: ${data.professional_license[0]}`;
      else if (data.curp) msg = `CURP: ${data.curp[0]}`;
      else if (data.detail) msg = data.detail;

      errorMessage.value = msg;
      errorPopup.value = true;
    } else {
      errorMessage.value = 'Ocurrió un error desconocido. Inténtelo de nuevo.';
      errorPopup.value = true;
    }
  } finally {
    loading.value = false;
  }
}

const goToLogin = () => {
  router.push('/login')
}

const closeErrorPopup = () => {
  errorPopup.value = false
  errorMessage.value = ''
}
</script>
