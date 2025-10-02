<template>
  <div class="flex flex-col items-center justify-center p-6 bg-gray-50 dark:bg-gray-900">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-sm">
      <ul class="space-y-4">
        <li @click="openModal('delete')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
          <IconTrash class="w-7 h-7 text-gray-600 dark:text-gray-400" />
          <span class="text-gray-800 text-lg dark:text-gray-200">Eliminación de la cuenta</span>
        </li>
        <li @click="openModal('password')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
          <IconLock class="w-7 h-7 text-gray-600 dark:text-gray-400" />
          <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar contraseña</span>
        </li>
        <li @click="openModal('email')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
          <IconMail class="w-7 h-7 text-gray-600 dark:text-gray-400" />
          <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar correo electrónico</span>
        </li>
        <li @click="openModal('alias')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
          <IconEdit class="w-7 h-7 text-gray-600 dark:text-gray-400" />
          <span class="text-gray-800 text-lg dark:text-gray-200">Editar alias</span>
        </li>
        <li class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
          <button
            @click="theme.toggleDark"
            class="rounded-full border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 px-4 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-200 transition-all duration-200 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105"
          >
            {{ theme.isDark ? '🌙 ' : '☀️ ' }}
          </button>
          <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar tema</span>
        </li> 
      </ul>
    </div>

    <!-- Modal para eliminar cuenta -->
    <div v-if="activeModal === 'delete'" class="fixed inset-0 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300">
        <h3 class="text-xl font-bold mb-4 text-center dark:text-white">Eliminar cuenta</h3>
        <p class="text-sm text-center text-gray-600 dark:text-gray-400 mb-6">Esta acción es irreversible, todos los datos asociados a tu cuenta serán eliminados permanentemente.</p>
        <form @submit.prevent="deleteAccount">
          <div class="mb-4">
            <label for="password-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contraseña actual</label>
            <input type="password" id="password-confirm" v-model="deletePassword" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Contraseña">
          </div>
          <div class="mb-6">
            <label for="password-reconfirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirmación de contraseña</label>
            <input type="password" id="password-reconfirm" v-model="deletePasswordConfirm" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Confirmación de contraseña">
          </div>
          <p v-if="deleteError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ deleteError }}</p>
          <div class="flex flex-col space-y-4">
            <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Confirmar</button>
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDeleteSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
        <h3 class="text-xl font-bold mb-4 dark:text-white">Eliminar cuenta</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">¡Tu cuenta ha sido eliminada satisfactoriamente!</p>
        <div class="flex justify-center mb-4">
          <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <button @click="closeDeleteSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
      </div>
    </div>

    <!-- Modal para cambiar la contraseña -->
    <div v-if="activeModal === 'password'" class="fixed inset-0 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300">
        <h3 class="text-xl font-bold mb-4 dark:text-white text-center">Cambiar contraseña</h3>
        <p class="text-sm text-center text-gray-600 dark:text-gray-400 mb-4">
          Recuerda que la contraseña debe cumplir con:
          <ul class="list-disc list-inside mt-2 text-left dark:text-white">
            <li>- Longitud de 8 a 32 caracteres.</li>
            <li>- Al menos una mayúscula.</li>
            <li>- Al menos un número.</li>
            <li>- Al menos un carácter especial.</li>
          </ul>
        </p>
        <form @submit.prevent="changePassword">
          <div class="mb-4">
            <label for="current-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contraseña actual</label>
            <input type="password" id="current-password" v-model="currentPassword" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          </div>
          <div class="mb-4">
            <label for="new-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nueva contraseña</label>
            <input type="password" id="new-password" v-model="newPassword" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          </div>
          <div class="mb-4">
            <label for="new-password-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirmación de la nueva contraseña</label>
            <input type="password" id="new-password-confirm" v-model="newPasswordConfirm" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          </div>
          <p v-if="passwordError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ passwordError }}</p>
          <div class="flex flex-col space-y-4">
            <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Confirmar</button>
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Modal para cambiar correo electrónico -->
    <div v-if="activeModal === 'email'" class="fixed inset-0 flex items-center justify-center z-50">
  <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full">
    <h3 class="text-xl font-bold mb-4 dark:text-white text-center">Cambiar correo electrónico</h3>

    <form v-if="emailStep === 1" @submit.prevent="sendVerificationCode">
      <p class="text-sm text-center text-gray-600 dark:text-gray-400 mb-4">
        Para confirmar tu identidad, introduce tu contraseña actual y el nuevo correo.
      </p>
      
      <div class="mb-4">
        <label for="current-password-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contraseña actual</label>
        <input type="password" id="current-password-email" v-model="currentPasswordEmail" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" required>
      </div>
      <div class="mb-4">
        <label for="new-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nuevo correo electrónico</label>
        <input type="email" id="new-email" v-model="newEmail" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" required>
      </div>
      <p v-if="emailError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ emailError }}</p>
      <div class="flex justify-end space-x-4">
        <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
        <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Enviar Código</button>
      </div>
    </form>

    <form v-else @submit.prevent="changeEmail" class="text-center">
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Se envió un código de verificación a: **{{ newEmail }}**.
        <span class="block text-sm font-semibold mt-2" :class="{'text-red-500': timeRemaining <= 60, 'text-green-600 dark:text-green-400': timeRemaining > 60}">
          Expira en: {{ formattedTime }}
        </span>
      </p>

      <div class="mb-4">
        <label for="verification-code" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Ingresa el código</label>
        <input type="text" id="verification-code" v-model="verificationCode" class="mt-1 block w-full border rounded-md shadow-sm p-2 text-center dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Código" :disabled="isCodeInvalidated" required>
      </div>

      <p v-if="verificationError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ verificationError }}</p>

      <div class="flex flex-col space-y-4">
        <button type="submit" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-semibold" :disabled="isCodeInvalidated">
          Verificar código
        </button>

        <button 
          type="button" 
          @click="sendVerificationCode" 
          :disabled="!canResendCode"
          class="px-4 py-2 font-semibold rounded transition-all duration-200"
          :class="{
            'bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-300': canResendCode,
            'bg-gray-100 text-gray-400 dark:bg-gray-800 cursor-not-allowed': !canResendCode
          }"
        >
          {{ isCodeInvalidated ? 'Código invalidado' : canResendCode ? `Reenviar Código (${resendAttempts}/${maxResendAttempts})` : 'Límite de reenvío alcanzado' }}
        </button>
        
        <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">
          Cancelar y reiniciar
        </button>
      </div>
    </form> 
  </div>
</div>

  <!-- Modal para cambiar alias -->
    <div v-if="activeModal === 'alias'" class="fixed inset-0 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full">
        <h3 class="text-xl font-bold mb-4 dark:text-white">Editar alias</h3>
        <p class="text-sm text-center text-gray-600 dark:text-gray-400 mb-4">
          Recuerda que el alias debe cumplir con:
          <ul class="list-disc list-inside mt-2 text-left dark:text-white">
            <li>- Longitud de 1 a 40 caracteres.</li>
            <li>- No consisitir sólo en espacios.</li>
            <li>- Al menos un número.</li>
            <li>- Al menos un carácter especial.</li>
          </ul>
        </p>
        <form @submit.prevent="editAlias">
          <div class="mb-4">
            <label for="new-alias" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nuevo alias</label>
            <input type="text" id="new-alias" v-model="newAlias" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          </div>
          <p v-if="aliasError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ aliasError }}</p>
          <div class="flex justify-end space-x-4">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
            <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
        <h3 class="text-xl font-bold mb-4 dark:text-white">{{ successTitle }}</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">{{ successMessage }}</p>
        <div class="flex justify-center mb-4">
          <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <button @click="closeSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
      </div>
    </div>

    <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center border border-gray-400">
        <h3 class="text-xl font-bold text-red-500 mb-4">¡Error!</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">{{ errorMessage }}</p>
        <button @click="closeErrorModal" class="px-6 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg w-full">Entendido</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { IconLock, IconTrash, IconMail, IconEdit } from "@tabler/icons-vue";
import { useThemeStore } from '@/store/theme'

const theme = useThemeStore()

const router = useRouter();

// Variables para controlar los modales
const activeModal = ref<string | null>(null);
const showSuccessModal = ref(false);
const showDeleteSuccessModal = ref(false);
const showErrorModal = ref(false);

// Variables para los formularios y mensajes
const successTitle = ref("");
const successMessage = ref("");
const errorMessage = ref("");

const emailStep = ref(1); // 1: Pedir datos, 2: Verificar código
const currentPasswordEmail = ref(""); // Contraseña actual para el flujo de correo
const verificationCode = ref(""); // Código que el usuario ingresa
const verificationError = ref<string | null>(null); // Error específico para la verificación

// -- NUEVAS VARIABLES DE SEGURIDAD Y REINTENTOS PARA EL EMAIL --
const resendAttempts = ref(0);
const maxResendAttempts = 5; // Máximo 5 reenvíos permitidos
const verificationAttempts = ref(0);
const maxVerificationAttempts = 3; // Máximo 3 intentos de verificación fallidos
const isCodeInvalidated = ref(false); // Bandera para invalidación por 3 intentos
const codeSentTime = ref<number | null>(null); // Timestamp del envío
const CODE_EXPIRY_MINUTES = 5; // Duración máxima de 5 minutos

// Para el control de tiempo en la interfaz
const timeRemaining = ref(0); // Segundos restantes para el contador
let countdownTimer: number | null = null; // Variable para el setInterval

// Computed para mostrar el estado del botón de reenvío
const canResendCode = computed(() => {
    // Si ya tiene el código invalidado O ya usó los 5 reenvíos
    return resendAttempts.value < maxResendAttempts && !isCodeInvalidated.value;
});

// Computed para el formato de tiempo (M:SS)
const formattedTime = computed(() => {
    const minutes = Math.floor(timeRemaining.value / 60);
    const seconds = timeRemaining.value % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
});


const currentPassword = ref("");
const newPassword = ref("");
const newPasswordConfirm = ref(""); 
const newEmail = ref("");
const newAlias = ref("");
const deletePassword = ref("");
const deletePasswordConfirm = ref("");

// Variables para errores específicos de formulario
const deleteError = ref<string | null>(null);
const passwordError = ref<string | null>(null);
const emailError = ref<string | null>(null);
const aliasError = ref<string | null>(null);

// Función para abrir el modal correcto
function openModal(modalName: string) {
  activeModal.value = modalName;
  // Limpiar errores específicos al abrir
  deleteError.value = null;
  passwordError.value = null;
  emailError.value = null;
  aliasError.value = null;
}

// Función para cerrar cualquier modal
function closeModal() {
  activeModal.value = null;
  // Limpiar los valores de los formularios al cerrar
  currentPassword.value = "";
  newPassword.value = "";
  newPasswordConfirm.value = "";
  newEmail.value = "";
  newAlias.value = "";
  deletePassword.value = "";
  deletePasswordConfirm.value = "";
  // Limpiar errores específicos al cerrar
  deleteError.value = null;
  passwordError.value = null;
  emailError.value = null;
  aliasError.value = null;

  // Limpieza específica del flujo de correo
  currentPasswordEmail.value = "";
  verificationCode.value = "";
  emailStep.value = 1; // ¡Importante! Reiniciar el paso
  verificationError.value = null;
  emailError.value = null;
  resetEmailFlow(); // Usar la nueva función de reseteo para el modal de email

  closeErrorModal();
  closeSuccessModal();
  showDeleteSuccessModal.value = false;
}

function closeErrorModal() {
  showErrorModal.value = false;
  errorMessage.value = "";
}

function closeSuccessModal() {
  showSuccessModal.value = false;
  successTitle.value = "";
  successMessage.value = "";
}

// ----------------------------------------------------
// Funciones de manejo de datos (simuladas)
// ----------------------------------------------------

//Borrar cuenta*****************************************
async function deleteAccount() {
  if (deletePassword.value !== deletePasswordConfirm.value) {
    deleteError.value = "Las contraseñas no coinciden. Inténtalo de nuevo.";
    return;
  } else if (deletePassword.value.length === 0 || deletePasswordConfirm.value.length === 0) {
    deleteError.value = "Por favor, completa ambos campos de contraseña.";
    return;
  }

  deleteError.value = null;

  try {
    // Simulación: lanzar error si la contraseña es "error"
    if (deletePassword.value === "error") {
      throw new Error("La contraseña proporcionada es incorrecta.");
    }
    
    console.log("Simulando eliminación de cuenta...");
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("Contraseña enviada:", deletePassword.value);
    
    closeModal();
    showDeleteSuccessModal.value = true;
  } catch (err: unknown) {
    console.error(err);
    const error = err as Error;
    errorMessage.value = error.message || "Hubo un problema al eliminar la cuenta. Por favor, inténtalo de nuevo.";
    showErrorModal.value = true;
  }
}
//borrar cuenta, eliminar datos del local storage - cerrar modal y redirigir a login
function closeDeleteSuccessModal() {
  showDeleteSuccessModal.value = false;
  localStorage.removeItem('authToken');
  localStorage.removeItem('userProfile');
  router.push('/login');
}

//Cambiar contraseña*****************************************
async function changePassword() {
  // Validaciones del frontend
  if (!currentPassword.value || !newPassword.value || !newPasswordConfirm.value) {
    passwordError.value = "Por favor, completa todos los campos.";
    return;
  }
  if (newPassword.value !== newPasswordConfirm.value) {
    passwordError.value = "La nueva contraseña y su confirmación no coinciden.";
    return;
  }
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$/;
  if (!passwordRegex.test(newPassword.value)) {
    passwordError.value = "La contraseña no cumple con los requisitos de seguridad.";
    return;
  }

  passwordError.value = null;

  try {
    // Simulación: lanzar error si la contraseña actual es "error"
    if (currentPassword.value === "error") {
      throw new Error("La contraseña actual es incorrecta.");
    }
    
    console.log("Simulando cambio de contraseña...");
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("Contraseña actual:", currentPassword.value);
    console.log("Nueva contraseña:", newPassword.value);
    
    closeModal();
    successTitle.value = "Contraseña actualizada";
    successMessage.value = "Tu contraseña ha sido actualizada con éxito.";
    showSuccessModal.value = true;
  } catch (err: unknown) {
    console.error(err);
    const error = err as Error;
    errorMessage.value = error.message || "Hubo un problema al cambiar la contraseña.";
    showErrorModal.value = true;
  }
}

//Cambiar correo*****************************************
function startCountdown() {
    // Iniciar con 5 minutos (300 segundos)
    timeRemaining.value = CODE_EXPIRY_MINUTES * 60;
    if (countdownTimer) clearInterval(countdownTimer);

    countdownTimer = setInterval(() => {
        if (timeRemaining.value > 0) {
            timeRemaining.value--;
        } else {
            // El tiempo ha expirado
            clearInterval(countdownTimer as number);
            countdownTimer = null;
        }
    }, 1000) as unknown as number;
}

// Función para reiniciar el flujo completo del email
function resetEmailFlow() {
  //detener el contador primero
  if (countdownTimer) {
        clearInterval(countdownTimer);
        countdownTimer = null;
    }
    // Reiniciar todas las variables relacionadas con el flujo de seguridad
    resendAttempts.value = 0;
    verificationAttempts.value = 0;
    isCodeInvalidated.value = false;
    codeSentTime.value = null;
    emailStep.value = 1;
    currentPasswordEmail.value = "";
    verificationCode.value = "";
    emailError.value = null;
    verificationError.value = null;
    
}

// Lógica para enviar el código de verificación
// Función para enviar/reenviar el código
async function sendVerificationCode() {
    if (!currentPasswordEmail.value || !newEmail.value) {
        emailError.value = "Por favor, completa la contraseña y el nuevo correo.";
        return;
    }

    if (isCodeInvalidated.value) {
        emailError.value = "El código anterior fue invalidado. Cancela y reinicia el proceso.";
        return;
    }

    // Comprobación de límite de reenvío (solo para reenvío)
    if (resendAttempts.value >= maxResendAttempts && emailStep.value === 2) {
        emailError.value = `Has excedido el límite de ${maxResendAttempts} reenvíos. Reinicia el proceso.`;
        return;
    }

    emailError.value = null;

    try {
        // --- SIMULACIÓN DE API call para enviar código ---
        if (currentPasswordEmail.value === "error") {
            throw new Error("Contraseña actual incorrecta.");
        }
        await new Promise((resolve) => setTimeout(resolve, 1000));
        
        // Si la llamada es exitosa:
        codeSentTime.value = Date.now();
        
        if (emailStep.value === 2) { // Es un reenvío
             resendAttempts.value++;
             // Resetear intentos de verificación al enviar nuevo código
             verificationAttempts.value = 0; 
             verificationError.value = null;
        }

        emailStep.value = 2;
        verificationCode.value = "";
        verificationError.value = null;
        startCountdown(); // Iniciar el contador

    } catch (err: unknown) {
        const error = err as Error;
        emailError.value = error.message || "Error al enviar el código. Inténtalo de nuevo.";
    }
}

// Lógica para cambiar el correo (Paso 2: Verificar Código)
// Función para verificar el código
async function changeEmail() {
    if (verificationCode.value.length === 0) {
        verificationError.value = "Por favor, introduce el código.";
        return;
    }

    verificationError.value = null;

    // 1. CHEQUEO DE EXPIRACIÓN (5 minutos)
    const currentTime = Date.now();
    const expiryTimestamp = (codeSentTime.value || 0) + CODE_EXPIRY_MINUTES * 60 * 1000;

    if (currentTime > expiryTimestamp || timeRemaining.value <= 0) {
        verificationError.value = "El código de verificación ha expirado (5 minutos). Por favor, solicita uno nuevo.";
        // Simular que el código en el backend queda invalidado por tiempo.
        isCodeInvalidated.value = true;
        return; 
    }
    
    // 2. CHEQUEO DE CÓDIGO INVALIDADO POR INTENTOS
    if (isCodeInvalidated.value) {
        verificationError.value = `Código invalidado por ${maxVerificationAttempts} intentos fallidos. Cancela y reinicia el proceso.`;
        return;
    }

    try {
        // --- SIMULACIÓN DE BACKEND ---
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Simular código incorrecto
        if (verificationCode.value !== "123456") {
            // 3. LÓGICA DE INTENTOS FALLIDOS (Invalidación después de 3)
            verificationAttempts.value++;
            
            if (verificationAttempts.value >= maxVerificationAttempts) {
                isCodeInvalidated.value = true;
                throw new Error(`Código incorrecto. El código ha sido invalidado después de ${maxVerificationAttempts} intentos. Reinicia el proceso.`);
            } else {
                throw new Error(`Código incorrecto. Te quedan ${maxVerificationAttempts - verificationAttempts.value} intentos.`);
            }
        }
        // --- FIN DE SIMULACIÓN ---

        // Éxito:
        if (countdownTimer) clearInterval(countdownTimer);
        closeModal();
        successTitle.value = "Correo actualizado";
        successMessage.value = `Tu correo electrónico ha sido actualizado a ${newEmail.value} con éxito.`;
        showSuccessModal.value = true;
        resetEmailFlow(); // Reiniciar todas las variables
        
    } catch (err: unknown) {
        const error = err as Error;
        
        // Manejar el error específico de intentos agotados
        if (error.message.includes("Código incorrecto. El código ha sido invalidado")) {
            verificationError.value = error.message;
        } else if (error.message.includes("Código incorrecto")) {
            verificationError.value = error.message;
        } else {
            verificationError.value = "La verificación falló. Revisa tu código.";
        }
    }
}

/* 
respuesta simulada error por expiración del código
{
  "error_type": "EXPIRED_CODE",
  "message": "El código de verificación ha expirado. Por favor, solicita uno nuevo."
}*/

//Editar alias*****************************************
async function editAlias() {
  if (newAlias.value.length === 0) {
    aliasError.value = "Por favor, completa el campo.";
    return;
  }
  if (newAlias.value.length > 40) {
    aliasError.value = "El alias no puede exceder los 40 caracteres.";
    return;
  }
  if (newAlias.value.trim() === "") {
    aliasError.value = "El alias no puede consistir solo en espacios.";
    return;
  }
  aliasError.value = null;
  
  try {
    if (newAlias.value === "error") {
      throw new Error("El alias no es válido.");
    }

    console.log("Simulando edición de alias...");
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("Nuevo alias:", newAlias.value);

    closeModal();
    successTitle.value = "Alias actualizado";
    successMessage.value = "Tu alias ha sido actualizado con éxito.";
    showSuccessModal.value = true;
  } catch (err: unknown) {
    console.error(err);
    const error = err as Error;
    errorMessage.value = error.message || "Hubo un problema al editar el alias.";
    showErrorModal.value = true;
  }
}
</script>