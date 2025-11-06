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
          {{ title }}
        </h1>

          <p v-if="errorMessage" class="text-sm text-red-500 text-center mb-4 font-semibold">{{ errorMessage }}</p>

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
              :disabled="loading"
            >
              {{ loading ? 'Verificando y logueando...' : 'Iniciar sesión' }}
            </button>
            <button
              @click.prevent="resendCode"
              class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
              :disabled="loading"
            >
              Volver a enviar código {{ remainingTimeFormatted }}
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

  <div v-if="successPopup" class="fixed inset-0 flex items-center justify-center z-50">
  <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center">
    <div class="flex flex-col items-center justify-center">
      <IconCircleCheckFilled class="text-green-500 w-16 h-16 mb-4" />
      <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">¡Éxito!</h3>
      <p class="text-gray-600 dark:text-gray-300 mb-4">
        Tu cuenta ha sido activada correctamente. Serás redirigido en unos segundos...
      </p>
      <button
        @click="closeSuccessPopup"
        class="bg-green-500 text-white font-semibold py-2 px-6 rounded-lg hover:bg-green-600 transition-colors"
      >
        Ir ahora
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
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  IconLockSquareRounded,
  IconMail,
  IconAlertCircle,
  IconCircleXFilled,
  IconCircleCheckFilled,
} from '@tabler/icons-vue';
import WomanHeart from '../components/WomanHeart.vue';
import { isAxiosError } from 'axios';
import * as AuthServices from '@/modules/auth/services/authServices';
import { useAuthStore, type UserType } from '@/store/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// --- Lógica de Título Dinámico ---
const userType = computed(() => route.params.type as string);
const title = computed(() => {
  if (userType.value === 'professional') {
    return 'Activación de Cuenta de Terapeuta';
  }
  return 'Activa tu cuenta de Paciente';
});

// --- Refs del Formulario y Popups ---
const email = ref('');
const password = ref('');
const validationCode = ref('');
const loading = ref(false);
const errorPopup = ref(false);
const successPopup = ref(false);
const resendPopup = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// --- Lógica del Temporizador para Reenvío ---
const lastResendTimestamp = ref(0);
const currentTime = ref(Date.now());
const fiveMinutesInMs = 5 * 60 * 1000;
let timeInterval: number | null = null;

// 1. COMPUTED ORIGINAL (Devuelve un NÚMERO)
//    Este lo usa 'isResendDisabled'
const remainingTime = computed(() => {
  if (lastResendTimestamp.value === 0) return 0;
  const elapsed = currentTime.value - lastResendTimestamp.value;
  // Devuelve los milisegundos restantes
  return Math.max(0, fiveMinutesInMs - elapsed);
});

// 2. COMPUTED PARA FORMATEAR (Devuelve un STRING)
//    Este lo usa el botón en el template
const remainingTimeFormatted = computed(() => {
  if (remainingTime.value <= 0) return ''; // Lee del computed original

  const totalSeconds = Math.ceil(remainingTime.value / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const paddedSeconds = seconds < 10 ? `0${seconds}` : seconds;

  return ` (${minutes}:${paddedSeconds})`;
});

// 3. COMPUTED DE DESHABILITADO (Ahora funciona)
//    Lee el 'remainingTime' numérico
const isResendDisabled = computed(() => remainingTime.value > 0);



onMounted(() => {
  const emailFromUrl = route.query.email;
  if (emailFromUrl) {
    email.value = String(emailFromUrl);
  }
  // Inicia un intervalo para actualizar el tiempo actual cada segundo
  timeInterval = setInterval(() => {
    currentTime.value = Date.now();
  }, 1000);
});

onUnmounted(() => {
  // Limpia el intervalo cuando el componente se destruye
  if (timeInterval) {
    clearInterval(timeInterval);
  }
});

const isEmailValid = (email: string): boolean => {
  const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  return re.test(String(email).toLowerCase());
};

const firstTimeLogin = async () => {
  if (!isEmailValid(email.value)) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico con un formato válido.';
    errorPopup.value = true;
    return;
  }

  loading.value = true;
  errorMessage.value = '';
  try {
    const activationPayload = { email: email.value, password: password.value, verification_code: validationCode.value };

    if (userType.value === 'patient') {
      const response = await AuthServices.activateAccount(activationPayload);
      authStore.setTokens(response.data.access, response.data.refresh);
      authStore.setUserData(response.data.user.role as UserType);
      successMessage.value = '¡Cuenta activada! Serás redirigido a tu panel.';
      successPopup.value = true;
    } else { // Flujo para Profesional
      await AuthServices.verifyProfessionalEmail(activationPayload);
      successMessage.value = '¡Correo verificado! Ahora serás redirigido para que inicies sesión.';
      successPopup.value = true;
    }
  } catch (error: unknown) {
    if (isAxiosError(error) && error.response) {
      errorMessage.value = error.response.data.error || 'Credenciales o código incorrectos.';
    } else {
      errorMessage.value = 'Ocurrió un error desconocido.';
    }
    errorPopup.value = true;
  } finally {
    loading.value = false;
  }
};

const resendCode = async () => {
  if (isResendDisabled.value) {
    // 1. Calcula el total de segundos restantes (redondeando hacia arriba)
    const totalSeconds = Math.ceil(remainingTime.value / 1000);

    // 2. Obtiene los minutos y segundos
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    // 3. Crea el mensaje de espera
    let waitMessage = "Debes esperar ";
    if (minutes > 0) {
      waitMessage += `${minutes} minuto${minutes !== 1 ? 's' : ''}`;
      if (seconds > 0) {
        waitMessage += ` y ${seconds} segundo${seconds !== 1 ? 's' : ''}`;
      }
    } else {
      // Si no hay minutos, solo muestra los segundos
      waitMessage += `${seconds} segundo${seconds !== 1 ? 's' : ''}`;
    }

    errorMessage.value = `${waitMessage}.`;
    errorPopup.value = true;
    return;
  }
  if (!isEmailValid(email.value)) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico válido.';
    errorPopup.value = true;
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    const payload: { email: string, role: string, password?: string } = {
      email: email.value,
      role: userType.value,
    };

    // Si es profesional, añadimos la contraseña (requerida por tu backend para seguridad)
    if (userType.value === 'professional') {
      if (!password.value) {
        errorMessage.value = 'La contraseña es necesaria para reenviar el código de profesional.';
        errorPopup.value = true;
        loading.value = false;
        return;
      }
      payload.password = password.value;
    }

    await AuthServices.resendActivationCode(payload);

    resendPopup.value = true;
    lastResendTimestamp.value = Date.now();

  } catch (error) {
    if (isAxiosError(error) && error.response) {
      errorMessage.value = error.response.data.error || 'No se pudo reenviar el código.';
    } else {
      errorMessage.value = 'Ocurrió un error desconocido.';
    }
    errorPopup.value = true;
  } finally {
    loading.value = false;
  }
};

const closeErrorPopup = () => {
  errorPopup.value = false;
  errorMessage.value = '';
};

const closeSuccessPopup = async () => { // 1. Haz la función async
  successPopup.value = false;

  if (userType.value === 'patient') {
    try {
      // 2. Carga el perfil completo del usuario ANTES de redirigir
      await authStore.fetchUserProfile();

      // 3. Comprueba el estado de vinculación desde el store
      //    (Asumiendo que tu store tiene un getter 'isLinked'
      //     o puedes checar 'authStore.userProfile.is_linked')
      if (authStore.isLinked) {
        router.push({ name: 'home-patient' });
      } else {
        // 4. Si no está vinculado, envíalo a la página de vinculación
        router.push({ name: 'link-professional' });
      }
    } catch (error) {
      console.error('Error al cargar el perfil del paciente:', error);
      // Si falla la carga del perfil, envíalo al login
      router.push({ name: 'login' });
    }

  } else {
    // Si es profesional, simplemente va al login para que inicie sesión
    router.push({ name: 'login' });
  }
};

const closeResendPopup = () => {
  resendPopup.value = false;
};

</script>
