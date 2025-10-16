<template>
  <div v-if="props.activeModal === 'password'" class="fixed inset-0 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300">
      <h3 class="text-xl font-bold mb-4 dark:text-white text-center">Cambiar contraseña</h3>
      <div class="text-sm text-left text-gray-600 dark:text-gray-400 mb-4">
        <p v-for="req in passwordValidation" :key="req.text" class="transition-colors" :class="{'text-green-500': req.met, 'text-red-500': !req.met && newPassword.length > 0}">
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
          <label for="new-password-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirmación</label>
          <input type="password" id="new-password-confirm" v-model="newPasswordConfirm" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        </div>
        <p v-if="passwordError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ passwordError }}</p>
        <div class="flex flex-col space-y-4">
          <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Confirmar</button>
          <button type="button" @click="emit('close')" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
        </div>
      </form>
    </div>
  </div>

  <div v-if="props.activeModal === 'email'" class="fixed inset-0 flex items-center justify-center z-50 p-4">
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
          <button type="button" @click="emit('close')" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
          <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold">Enviar Código</button>
        </div>
      </form>
      <form v-else @submit.prevent="changeEmail" class="text-center">
        <p class="text-gray-600 dark:text-gray-400 mb-4">Se envió un código a: <strong>{{ newEmail }}</strong>.</p>
        <span class="block text-sm font-semibold mb-4" :class="{'text-red-500': timeRemaining <= 0, 'text-green-500': timeRemaining > 0}">
          Expira en: {{ formattedTime }}
        </span>
        <div class="mb-4">
          <label for="verification-code" class="sr-only">Código</label>
          <input type="text" id="verification-code" v-model="verificationCode" class="mt-1 block w-full border rounded-md shadow-sm p-2 text-center dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Código de 6 dígitos" required :disabled="isCodeInvalidated">
        </div>
        <p v-if="verificationError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ verificationError }}</p>
        <div class="flex flex-col space-y-4">
          <button type="submit" class="px-4 py-2 bg-[#7DBFF8] text-white rounded font-semibold" :disabled="isCodeInvalidated">Verificar Código</button>
          <button type="button" @click="sendVerificationCode" :disabled="!canResendCode" class="px-4 py-2 font-semibold rounded" :class="{'bg-gray-200 hover:bg-gray-300': canResendCode, 'bg-gray-100 text-gray-400 cursor-not-allowed': !canResendCode}">
            {{ isCodeInvalidated ? 'Código invalidado' : canResendCode ? `Reenviar (${resendAttempts}/${maxResendAttempts})` : 'Límite alcanzado' }}
          </button>
          <button type="button" @click="emit('close')" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded">Cancelar y Reiniciar</button>
        </div>
      </form>
    </div>
  </div>

  <div v-if="props.activeModal === 'delete'" class="fixed inset-0 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300">
      <h3 class="text-xl font-bold mb-4 text-center dark:text-white">Eliminar cuenta</h3>
      <p class="text-sm text-center text-gray-600 dark:text-gray-400 mb-6">Esta acción es irreversible. Para confirmar, introduce tu contraseña.</p>
      <form @submit.prevent="deleteAccount">
        <div class="mb-4">
          <label for="delete-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contraseña actual</label>
          <input type="password" id="delete-password" v-model="deletePassword" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Contraseña">
        </div>
        <div class="mb-6">
            <label for="delete-password-confirm" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirmar contraseña</label>
            <input type="password" id="delete-password-confirm" v-model="deletePasswordConfirm" class="mt-1 block w-full border rounded-md shadow-sm p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Confirmar contraseña">
        </div>
        <p v-if="deleteError" class="text-red-500 text-sm mt-1 mb-4 text-center">{{ deleteError }}</p>
        <div class="flex flex-col space-y-4">
          <button type="submit" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-semibold">Confirmar Eliminación</button>
          <button type="button" @click="emit('close')" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import { isAxiosError } from "axios";
import {
  changePassword as apiChangePassword,
  requestEmailChange,
  confirmEmailChange,
  deleteAccount as apiDeleteAccount,
} from "@/modules/auth/services/authServices";

// --- Props y Emits ---
const props = defineProps<{ activeModal: string | null }>();
const emit = defineEmits<{
  (e: "close"): void;
  (e: "success", payload: { title: string; message: string }): void;
  (e: "error", payload: { message: string }): void;
  (e: "delete-success"): void;
}>();

const authStore = useAuthStore();

// --- Estado para Cambio de Contraseña ---
const currentPassword = ref("");
const newPassword = ref("");
const newPasswordConfirm = ref("");
const passwordError = ref<string | null>(null);

// --- Estado para Eliminar Cuenta ---
const deletePassword = ref("");
const deletePasswordConfirm = ref("");
const deleteError = ref<string | null>(null);

// --- Estado para Cambio de Email ---
const emailStep = ref(1);
const currentPasswordEmail = ref("");
const newEmail = ref("");
const verificationCode = ref("");
const emailError = ref<string | null>(null);
const verificationError = ref<string | null>(null);
const timeRemaining = ref(0);
let countdownTimer: number | null = null;

// --- Lógica de seguridad para el código de correo ---
const resendAttempts = ref(0);
const verificationAttempts = ref(0);
const isCodeInvalidated = ref(false);
const maxResendAttempts = 3;
const maxVerificationAttempts = 3;
const CODE_EXPIRY_MINUTES = 5;

// --- Propiedades Computadas ---
const passwordRequirements = [
    { regex: /[a-z]/, text: 'Al menos una letra minúscula' },
    { regex: /[A-Z]/, text: 'Al menos una letra mayúscula' },
    { regex: /\d/, text: 'Al menos un número' },
    { regex: /[@$!%*?&]/, text: 'Al menos un carácter especial' },
    { regex: /.{8,32}/, text: 'Entre 8 y 32 caracteres' }
];
const passwordValidation = computed(() => passwordRequirements.map(req => ({...req, met: req.regex.test(newPassword.value)})));
const isPasswordValid = computed(() => passwordValidation.value.every(req => req.met));
const formattedTime = computed(() => `${Math.floor(timeRemaining.value / 60)}:${(timeRemaining.value % 60).toString().padStart(2, '0')}`);
const canResendCode = computed(() => resendAttempts.value < maxResendAttempts && !isCodeInvalidated.value);

// --- Observador para limpiar formularios al cerrar ---
watch(() => props.activeModal, (newVal) => { if (newVal === null) resetAllForms(); });

function resetAllForms() {
  currentPassword.value = "";
  newPassword.value = "";
  newPasswordConfirm.value = "";
  passwordError.value = null;

  deletePassword.value = "";
  deletePasswordConfirm.value = "";
  deleteError.value = null;

  emailStep.value = 1;
  currentPasswordEmail.value = "";
  newEmail.value = "";
  verificationCode.value = "";
  emailError.value = null;
  verificationError.value = null;
  if(countdownTimer) clearInterval(countdownTimer);
  timeRemaining.value = 0;
  resendAttempts.value = 0;
  verificationAttempts.value = 0;
  isCodeInvalidated.value = false;
}

function startCountdown() {
  timeRemaining.value = CODE_EXPIRY_MINUTES * 60;
  if (countdownTimer) clearInterval(countdownTimer);
  countdownTimer = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      clearInterval(countdownTimer as number);
      isCodeInvalidated.value = true;
      verificationError.value = "El código ha expirado. Solicita uno nuevo.";
    }
  }, 1000) as unknown as number;
}

// --- Funciones de Lógica de Negocio ---

async function changePassword() {
  if (!currentPassword.value || !newPassword.value || !newPasswordConfirm.value) { passwordError.value = "Todos los campos son requeridos."; return; }
  if (newPassword.value !== newPasswordConfirm.value) { passwordError.value = "Las nuevas contraseñas no coinciden."; return; }
  if (!isPasswordValid.value) { passwordError.value = "La nueva contraseña no cumple los requisitos."; return; }
  passwordError.value = null;

  try {
    await apiChangePassword({ current_password: currentPassword.value, new_password: newPassword.value, new_password_confirm: newPasswordConfirm.value });
    emit("success", { title: "Contraseña Actualizada", message: "Tu contraseña ha sido actualizada con éxito." });
    emit("close");
  } catch (err) {
    if (isAxiosError(err) && err.response) {
      const errorData = err.response.data;
      passwordError.value = errorData.detail || errorData.current_password?.[0] || "Ocurrió un error.";
    } else {
      emit("error", { message: "No se pudo conectar con el servidor." });
    }
  }
}

async function sendVerificationCode() {
  if (!currentPasswordEmail.value || !newEmail.value) { emailError.value = "Por favor, completa ambos campos."; return; }
  if (isCodeInvalidated.value) { emailError.value = "El proceso fue invalidado. Por favor, reinicia."; return; }
  if (emailStep.value === 2 && resendAttempts.value >= maxResendAttempts) { emailError.value = `Límite de ${maxResendAttempts} reenvíos alcanzado.`; return; }
  emailError.value = null;

  try {
    await requestEmailChange({ current_password: currentPasswordEmail.value, new_email: newEmail.value });
    if (emailStep.value === 2) { // Si es un reenvío
      resendAttempts.value++;
      verificationAttempts.value = 0;
      verificationError.value = null;
    }
    emailStep.value = 2;
    startCountdown();
  } catch (err) {
    if (isAxiosError(err) && err.response) {
      const errorData = err.response.data;
      emailError.value = errorData.detail || errorData.current_password?.[0] || errorData.new_email?.[0] || "Ocurrió un error.";
    } else {
      emailError.value = "Error al conectar con el servidor.";
    }
  }
}

async function changeEmail() {
  if (timeRemaining.value <= 0) { verificationError.value = "El código ha expirado."; isCodeInvalidated.value = true; return; }
  if (isCodeInvalidated.value) { verificationError.value = `Proceso invalidado por ${maxVerificationAttempts} intentos fallidos.`; return; }
  if (!verificationCode.value) { verificationError.value = "Por favor, introduce el código."; return; }
  verificationError.value = null;

  try {
    await confirmEmailChange({ new_email: newEmail.value, verification_code: verificationCode.value });
    authStore.updateUserProfile({ email: newEmail.value });
    emit("success", { title: "Correo Actualizado", message: `Tu correo electrónico ha sido actualizado a ${newEmail.value}.` });
    emit("close");
  } catch (err) {
    verificationAttempts.value++;
    if (verificationAttempts.value >= maxVerificationAttempts) {
      isCodeInvalidated.value = true;
      verificationError.value = `Código incorrecto. Se invalidó tras ${maxVerificationAttempts} intentos.`;
    } else {
      if (isAxiosError(err) && err.response) {
        verificationError.value = err.response.data.detail || `Código incorrecto. Quedan ${maxVerificationAttempts - verificationAttempts.value} intentos.`;
      } else {
        verificationError.value = `Código incorrecto. Quedan ${maxVerificationAttempts - verificationAttempts.value} intentos.`;
      }
    }
  }
}

async function deleteAccount() {
  if (deletePassword.value !== deletePasswordConfirm.value) { deleteError.value = "Las contraseñas no coinciden."; return; }
  if (!deletePassword.value) { deleteError.value = "Por favor, introduce tu contraseña."; return; }
  deleteError.value = null;

  try {
    await apiDeleteAccount({ password: deletePassword.value });
    emit("delete-success");
    emit("close");
  } catch (err) {
    if (isAxiosError(err) && err.response) {
      deleteError.value = err.response.data.password?.[0] || err.response.data.detail || "La contraseña es incorrecta.";
    } else {
      emit("error", { message: "No se pudo conectar con el servidor." });
    }
  }
}
</script>
