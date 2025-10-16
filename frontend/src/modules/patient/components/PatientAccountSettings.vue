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
          Recuerda que la contraseña debe cumplir con:</p>
          <div class="text-sm text-left text-gray-600 dark:text-gray-400 mb-4">
            <p
                v-for="req in passwordValidation"
                :key="req.text"
                class="transition-colors"
                :class="{'text-green-500 dark:text-green-400': req.met, 'text-red-500 dark:text-red-400': !req.met && newPassword.length > 0}"
            >
                {{ req.met ? '✓' : '✗' }} {{ req.text }}
            </p>
        </div>
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
          Recuerda que el alias debe cumplir con:</p>
          <div class="text-sm text-left text-gray-600 dark:text-gray-400 mb-4">
            <p
                v-for="req in aliasValidation"
                :key="req.text"
                class="transition-colors"
                :class="{'text-green-500 dark:text-green-400': req.met, 'text-red-500 dark:text-red-400': !req.met && newAlias.length > 0}"
            >
                {{ req.met ? '✓' : '✗' }} {{ req.text }}
            </p>
        </div>

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
// import { useRouter } from "vue-router";
import { IconLock, IconTrash, IconMail, IconEdit } from "@tabler/icons-vue";
import { useThemeStore } from '@/store/theme'
import { updatePatientAlias, requestEmailChange, confirmEmailChange } from "@/modules/auth/services/authServices";
import { isAxiosError } from "axios";
import { useAuthStore } from "@/store/auth";
import { changePassword as apiChangePassword } from "@/modules/auth/services/authServices";
import { deleteAccount as apiDeleteAccount } from "@/modules/auth/services/authServices";
const authStore = useAuthStore();

const theme = useThemeStore()

// const router = useRouter();

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
    // Tus validaciones del frontend se mantienen
    if (deletePassword.value !== deletePasswordConfirm.value) {
        deleteError.value = "Las contraseñas no coinciden. Inténtalo de nuevo.";
        return;
    }
    if (deletePassword.value.length === 0) {
        deleteError.value = "Por favor, completa el campo de contraseña.";
        return;
    }
    deleteError.value = null;

    try {
        await apiDeleteAccount({ password: deletePassword.value });

        // Si la llamada es exitosa, el backend ya eliminó la cuenta.
        // Mostramos el modal de éxito final.
        closeModal();
        showDeleteSuccessModal.value = true;

    } catch (err: unknown) {
        console.error(err);
        if (isAxiosError(err) && err.response) {
            const errorData = err.response.data;
            if (errorData.password) {
                deleteError.value = errorData.password[0]; // Ej: "La contraseña es incorrecta."
            } else {
                deleteError.value = "Ocurrió un error al verificar tu contraseña.";
            }
        } else {
            errorMessage.value = "No se pudo conectar con el servidor.";
            showErrorModal.value = true;
        }
    }
}

//borrar cuenta, eliminar datos del local storage - cerrar modal y redirigir a login
function closeDeleteSuccessModal() {
  showDeleteSuccessModal.value = false;
  localStorage.removeItem('authToken');
  localStorage.removeItem('userProfile');
  authStore.logout();
}
  const passwordRequirements = [
    { regex: /[a-z]/, text: 'Al menos una letra minúscula' },
    { regex: /[A-Z]/, text: 'Al menos una letra mayúscula' },
    { regex: /\d/, text: 'Al menos un número' },
    { regex: /[@$!%*?&]/, text: 'Al menos un carácter especial (@$!%*?&)' },
    { regex: /.{8,32}/, text: 'Entre 8 y 32 caracteres de longitud' }
];

const passwordValidation = computed(() => {
    return passwordRequirements.map(req => {
        // .test() devuelve true si la contraseña cumple con la regex
        const isMet = req.regex.test(newPassword.value);
        return { ...req, met: isMet };
    });
});

const isPasswordValid = computed(() => passwordValidation.value.every(req => req.met));

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

  if (!isPasswordValid.value) {
        passwordError.value = "La contraseña no cumple con todos los requisitos de seguridad.";
        return;
    }

  passwordError.value = null;

  try {
        const payload = {
            current_password: currentPassword.value,
            new_password: newPassword.value,
            new_password_confirm: newPasswordConfirm.value,
        };

        await apiChangePassword(payload);

        // Si la llamada es exitosa:
        closeModal();
        successTitle.value = "Contraseña actualizada";
        successMessage.value = "Tu contraseña ha sido actualizada con éxito.";
        showSuccessModal.value = true;

    } catch (err: unknown) {
        console.error(err);
        if (isAxiosError(err) && err.response) {
            const errorData = err.response.data;
            // Mapeamos los errores del backend a nuestro 'ref' de error
            if (errorData.current_password) {
                passwordError.value = errorData.current_password[0];
            } else if (errorData.new_password) {
                passwordError.value = errorData.new_password[0];
            } else if (errorData.new_password_confirm) {
                passwordError.value = errorData.new_password_confirm[0];
            } else {
                passwordError.value = "Ocurrió un error inesperado. Inténtalo de nuevo.";
            }
        } else {
            // Error genérico si no es de Axios
            errorMessage.value = "No se pudo conectar con el servidor.";
            showErrorModal.value = true;
        }
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
async function sendVerificationCode() {
    if (!currentPasswordEmail.value || !newEmail.value) {
        emailError.value = "Por favor, completa la contraseña y el nuevo correo.";
        return;
    }
    // ... (tus otras validaciones de reintentos)
    emailError.value = null;

    try {
        await requestEmailChange({
            current_password: currentPasswordEmail.value,
            new_email: newEmail.value
        });

        // La lógica de éxito se mantiene igual
        codeSentTime.value = Date.now();
        if (emailStep.value === 2) {
            resendAttempts.value++;
            verificationAttempts.value = 0;
            verificationError.value = null;
        }
        emailStep.value = 2;
        verificationCode.value = "";
        startCountdown();

    } catch (err: unknown) {
        if (isAxiosError(err) && err.response) {
            const errorData = err.response.data;
            // Mostramos el error específico del backend
            emailError.value = errorData.detail || errorData.current_password?.[0] || errorData.new_email?.[0] || "Ocurrió un error.";
        } else {
            emailError.value = "Error al conectar con el servidor.";
        }
    }
}

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
        await confirmEmailChange({
          new_email: newEmail.value,
          verification_code: verificationCode.value
        });

        authStore.updateUserProfile({ email: newEmail.value });

        if (countdownTimer) clearInterval(countdownTimer);
        closeModal();
        successTitle.value = "Correo actualizado";
        successMessage.value = `Tu correo electrónico ha sido actualizado a ${newEmail.value} con éxito.`;
        showSuccessModal.value = true;
        resetEmailFlow();

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

//Editar alias*****************************************
const aliasRequirements = [
    { regex: /^.{1,40}$/, text: 'Entre 1 y 40 caracteres' },
    { regex: /^(?!\s*$).+/, text: 'No puede consistir solo en espacios' },
    { regex: /\d/, text: 'Debe contener al menos un número' },
    { regex: /[@$!%*?&]/, text: 'Debe contener un carácter especial (@$!%*?&)' }
];

const aliasValidation = computed(() => {
    return aliasRequirements.map(req => ({
        ...req,
        met: req.regex.test(newAlias.value)
    }));
});

const isAliasValid = computed(() => aliasValidation.value.every(req => req.met));

async function editAlias() {
  if (!isAliasValid.value) {
        aliasError.value = "Por favor, cumple con todos los requisitos para el alias.";
        return;
    }
  aliasError.value = null;

  try {
        await updatePatientAlias({ alias: newAlias.value });
        authStore.updateUserProfile({ alias: newAlias.value });

        // Si la llamada es exitosa, muestra el modal de éxito
        closeModal();
        successTitle.value = "Alias actualizado";
        successMessage.value = "Tu alias ha sido actualizado con éxito.";
        showSuccessModal.value = true;



    } catch (err: unknown) {
        console.error(err);
        // --- 3. MANEJO DE ERRORES REALES DE LA API ---
        if (isAxiosError(err) && err.response) {
            // Si el backend envía un error específico (por ejemplo, desde la validación del serializer)
            const errorData = err.response.data;
            if (errorData.alias && Array.isArray(errorData.alias)) {
                errorMessage.value = errorData.alias[0];
            } else {
                errorMessage.value = "Hubo un problema al editar el alias.";
            }
        } else {
            errorMessage.value = "Error de red o problema inesperado.";
        }
        showErrorModal.value = true;
    }
}
</script>
