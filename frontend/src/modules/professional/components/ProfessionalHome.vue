<template>
  <div class="grid flex-1 p-4 sm:p-8 md:p-16 dark:bg-gray-900">
    <div class="max-w-6xl mx-auto w-full">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start mb-12">
        <div class="lg:col-span-2 flex flex-col justify-between h-full">
          <div class="mb-12">
            <h1 class="text-5xl md:text-6xl text-gray-800 dark:text-white font-bold">
              {{ salutation }}
            </h1>
            <h1 class="text-6xl md:text-7xl font-light text-gray-900 mt-2 dark:text-white">
              {{ professionalName }}
            </h1>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full mb-12 border border-gray-200">
            <h2 class="text-2xl font-semibold mb-6 text-gray-900 dark:text-white border-b pb-2">Opciones de Cuenta y Configuración</h2>
            <ul class="space-y-4">
              <li @click="openSecurityModal('password')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-lock w-7 h-7 text-gray-600 dark:text-gray-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6z"></path><path d="M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0"></path><path d="M8 11v-4a4 4 0 0 1 8 0v4"></path></svg>
                <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar contraseña</span>
              </li>
              <li @click="openSecurityModal('email')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-mail w-7 h-7 text-gray-600 dark:text-gray-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z"></path><path d="M3 7l9 6l9 -6"></path></svg>
                <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar correo electrónico</span>
              </li>
              <li @click="openSecurityModal('delete')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-trash w-7 h-7 text-red-600 dark:text-red-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 7l16 0"></path><path d="M10 11l0 6"></path><path d="M14 11l0 6"></path><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path></svg>
                <span class="text-red-600 text-lg dark:text-red-400">Eliminación de la cuenta</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="flex flex-col items-center lg:items-end pt-4 space-y-4">
          <p class="text-xl font-light text-gray-600 mb-2 dark:text-white text-center lg:text-right">
            Aquí tienes tu código de enlace para compartir con tus pacientes:
          </p>
          <div class="flex items-center space-x-4">
            <span class="text-lg font-semibold text-gray-700 dark:text-white">Mi código:</span>
            <input type="text" :value="linkCode" readonly class="py-2 px-4 rounded-lg border text-lg font-mono tracking-widest text-center bg-gray-50 select-none w-auto dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          </div>
          <button @click="openConfirmationModal" class="px-6 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded-lg font-semibold w-full max-w-xs">
            Generar otro código
          </button>
          <img src="/src/assets/images/soporte_profesional.png" alt="Ilustración de soporte" class="w-full max-w-xs h-auto mt-4"/>
        </div>
      </div>

      <SecurityModals
        :active-modal="activeSecurityModal"
        @close="activeSecurityModal = null"
        @success="handleSuccess"
        @error="handleError"
        @delete-success="handleDeleteSuccess"
      />

      <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
          <h3 class="text-xl font-bold mb-4 dark:text-white">{{ successTitle }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">{{ successMessage }}</p>
          <button @click="showSuccessModal = false" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
        </div>
      </div>

      <div v-if="showErrorModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
          <h3 class="text-xl font-bold text-red-500 mb-4">¡Error!</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">{{ errorMessage }}</p>
          <button @click="showErrorModal = false" class="px-6 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg w-full">Cerrar</button>
        </div>
      </div>

      <div v-if="showDeleteSuccessModal" class="fixed inset-0 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
          <h3 class="text-xl font-bold mb-4 dark:text-white">Cuenta Eliminada</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">Tu cuenta ha sido eliminada permanentemente.</p>
          <button @click="closeDeleteSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
        </div>
      </div>

      <div v-if="showCodeModal" class="fixed inset-0 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
          <h3 class="text-xl font-bold mb-4 dark:text-white">Generar nuevo código</h3>
          <p class="text-gray-600 dark:text-gray-300 mb-8">¿Estás seguro? El código actual será invalidado.</p>
          <div class="flex flex-col space-y-3">
            <button @click="confirmCodeGeneration" class="px-4 py-3 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded-lg font-semibold">Confirmar</button>
            <button @click="showCodeModal = false" class="px-4 py-3 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
// import { useRouter } from "vue-router";
import { useAuthStore } from '@/store/auth';
import { storeToRefs } from 'pinia';
import * as AuthServices from '@/modules/auth/services/authServices';
import SecurityModals from '@/modules/auth/components/SecurityModals.vue';

// const router = useRouter();
const authStore = useAuthStore();

// --- Estado Reactivo del Store ---
const { userProfile } = storeToRefs(authStore);

// --- Estado Local de la Vista ---
const showCodeModal = ref(false);
// const showSuccessUpdateModal = ref(false); // Podrías fusionarlo con el showSuccessModal genérico
// const newGeneratedCode = ref('');

// --- Estado para Controlar Modales ---
const activeSecurityModal = ref<string | null>(null);
const showSuccessModal = ref(false);
const showDeleteSuccessModal = ref(false);
const showErrorModal = ref(false);
const successTitle = ref('');
const successMessage = ref('');
const errorMessage = ref('');

// --- Propiedades Computadas ---
const professionalName = computed(() => {
  if (!userProfile.value) return 'Cargando...';
  return `${userProfile.value.name} ${userProfile.value.paternal_last_name}`;
});

const salutation = computed(() => {
  const sex = (userProfile.value as AuthServices.ProfessionalProfile)?.sex?.toLowerCase();
  return sex === 'female' ? 'Bienvenida,' : 'Bienvenido,';
});

const linkCode = computed(() => {
  return (userProfile.value as AuthServices.ProfessionalProfile)?.link_code || 'N/A';
});

// --- Funciones para Código de Enlace ---
function openConfirmationModal() {
  showCodeModal.value = true;
}

async function confirmCodeGeneration() {
  showCodeModal.value = false;
  try {
    const response = await AuthServices.regenerateLinkCode();
    const newCode = response.data.new_link_code;

    // Actualizamos el estado global en Pinia
    authStore.updateUserProfile({ link_code: newCode });

    // Mostramos feedback de éxito
    handleSuccess({ title: '¡Código Actualizado!', message: `Tu nuevo código de enlace es: ${newCode}` });

  } catch (error) {
    console.error('Error al generar código:', error);
    handleError({ message: 'No se pudo generar un nuevo código. Intenta más tarde.' });
  }
}

// --- Funciones para Manejar Eventos de SecurityModals ---
function openSecurityModal(modalName: string) {
  activeSecurityModal.value = modalName;
}

function handleSuccess(payload: { title: string; message: string }) {
  successTitle.value = payload.title;
  successMessage.value = payload.message;
  showSuccessModal.value = true;
}

function handleError(payload: { message: string }) {
  errorMessage.value = payload.message;
  showErrorModal.value = true;
}

function handleDeleteSuccess() {
  showDeleteSuccessModal.value = true;
}

function closeDeleteSuccessModal() {
  showDeleteSuccessModal.value = false;
  authStore.logout(); // authStore se encarga de limpiar todo y redirigir
}
</script>
