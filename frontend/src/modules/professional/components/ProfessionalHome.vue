<template>
    <div class="grid flex-1 p-16 dark:bg-gray-900">
        <div class="max-w-6xl mx-auto">

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start mb-12">

                <div class="lg:col-span-2 flex flex-col justify-between h-full">

                    <div class="mb-12">
                        <h1 v-if="salutation === 'Bienvenido,'" class="text-6xl text-gray-800 dark:text-white font-bold">
                            Bienvenido,
                        </h1>
                        <h1 v-else class="text-6xl text-gray-800 dark:text-white font-bold">
                            Bienvenida,
                        </h1>
                        <h1 class="text-7xl font-light text-gray-900 mt-2 dark:text-white">
                            {{ professionalName }}
                        </h1>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full mb-12 border border-gray-200">
                        <h2 class="text-2xl font-semibold mb-6 text-gray-900 dark:text-white border-b pb-2">Opciones de Cuenta y configuración</h2>
                        <ul class="space-y-4">
                            <li @click="openSecurityModal('password')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-lock w-7 h-7 text-gray-600 dark:text-gray-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6z"></path><path d="M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0"></path><path d="M8 11v-4a4 4 0 0 1 8 0v4"></path></svg>
                                <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar contraseña</span>
                            </li>
                            <li @click="openSecurityModal('email')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-mail w-7 h-7 text-gray-600 dark:text-gray-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z"></path><path d="M3 7l9 6l9 -6"></path></svg>
                                <span class="text-gray-800 text-lg dark:text-gray-200">Cambiar correo electrónico</span>
                            </li>
                            <li @click="openSecurityModal('delete')" class="flex items-center space-x-4 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-200">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-trash w-7 h-7 text-red-600 dark:text-red-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 7l16 0"></path><path d="M10 11l0 6"></path><path d="M14 11l0 6"></path><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path></svg>
                                <span class="text-red-600 text-lg dark:text-red-400">Eliminación de la cuenta</span>
                            </li>
                        </ul>
                    </div>

                </div>

                <div class="flex flex-col items-end pt-4 space-y-4">
                    <p class="text-xl font-light text-gray-600 mb-2 dark:text-white py-4">
                        Aquí tienes tu código de enlace para compartir con tus pacientes:
                    </p>

                    <div class="flex items-center space-x-4">
                        <span class="text-lg font-semibold text-gray-700 dark:text-white">Mi código:</span>
                        <input
                            type="text"
                            :value="linkCode"
                            readonly
                            class="py-2 px-4 rounded-lg border border-gray-300 text-lg font-medium text-center bg-gray-50 select-none cursor-default w-auto dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>

                    <button
                        @click="openConfirmationModal"
                        :disabled="dailyCodeChanges >= maxDailyChanges"
                        class="px-6 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded-lg font-semibold transition-colors duration-300 shadow-md w-full max-w-xs disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Generar otro código
                    </button>
                    <p v-if="dailyCodeChanges >= maxDailyChanges" class="text-red-500 text-sm text-right">
                        Límite diario de cambios alcanzado ({{ dailyCodeChanges }}/{{ maxDailyChanges }})
                    </p>

                    <img
                        src="/src/assets/images/soporte_profesional.png"
                        alt="Ilustración de soporte"
                        class="w-auto h-auto mt-4"
                    />
                </div>
            </div>

            <div v-if="showCodeModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="fixed inset-0" @click="showCodeModal = false"></div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">Generar código de enlace nuevo</h3>
                    <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                        ¿Estás seguro de que deseas generar un nuevo código? El código actual será **invalidado** y los pacientes que deseen vincularse contigo deberán usar el nuevo código.
                        <span class="block font-semibold text-red-500 mt-2">Esta acción no se puede deshacer.</span>
                    </p>
                    <div class="flex flex-col space-y-3">
                        <button
                            @click="confirmCodeGeneration"
                            class="px-4 py-3 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded-lg font-semibold transition-colors"
                        >
                            Confirmar
                        </button>
                        <button
                            @click="showCodeModal = false"
                            class="px-4 py-3 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg transition-colors"
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>

            <div v-if="showSuccessUpdateModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="fixed inset-0" @click="showSuccessUpdateModal = false"></div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white text-green-500">¡Código de enlace actualizado!</h3>
                        <p class="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                            Tu nuevo código ha sido generado exitosamente. Por favor, compártelo con tus pacientes.
                        </p>
                    <div class="flex flex-col items-center justify-center mb-6">
                        <span class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Nuevo Código:</span>
                        <span class="text-2xl font-extrabold text-[#7DBFF8] tracking-widest bg-gray-100 dark:bg-gray-700 p-2 rounded-md">
                        {{ newGeneratedCode }}
                        </span>
                    </div>

                    <button
                        @click="showSuccessUpdateModal = false"
                        class="w-full px-4 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-semibold transition-colors"
                    >
                        Aceptar
                    </button>
                </div>
            </div>

            <div v-if="activeSecurityModal === 'delete'" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300 relative z-10 mx-4">
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
                            <button type="submit" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-semibold">Confirmar Eliminación</button>
                            <button type="button" @click="closeSecurityModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>

            <div v-if="showDeleteSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">Eliminar cuenta</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">¡Tu cuenta ha sido eliminada satisfactoriamente!</p>
                    <div class="flex justify-center mb-4">
                        <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        </div>
                    </div>
                    <button @click="closeDeleteSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
                </div>
            </div>


            <div v-if="activeSecurityModal === 'password'" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full border border-gray-300 relative z-10 mx-4">
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
                            <button type="button" @click="closeSecurityModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>

            <div v-if="activeSecurityModal === 'email'" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full relative z-10 mx-4">
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
                            <button type="button" @click="closeSecurityModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">Cancelar</button>
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
                            <button type="submit" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold" :disabled="isCodeInvalidated">
                                Verificar código
                            </button>

                            <button
                                type="button"
                                @click="resendCodeWithCheck"
                                :disabled="!canResendCode"
                                class="px-4 py-2 font-semibold rounded transition-all duration-200"
                                :class="{
                                    'bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-300': canResendCode,
                                    'bg-gray-100 text-gray-400 dark:bg-gray-800 cursor-not-allowed': !canResendCode
                                }"
                            >
                                {{ isCodeInvalidated ? 'Código invalidado' : canResendCode ? `Reenviar Código (${resendAttempts}/${maxResendAttempts})` : 'Límite de reenvío alcanzado' }}
                            </button>

                            <button type="button" @click="closeSecurityModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded">
                                Cancelar y reiniciar
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">{{ successTitle }}</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ successMessage }}</p>
                    <div class="flex justify-center mb-4">
                        <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        </div>
                    </div>
                    <button @click="closeSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
                </div>
            </div>

            <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center border border-gray-400 relative z-10 mx-4">
                    <h3 class="text-xl font-bold text-red-500 mb-4">¡Error!</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ errorMessage }}</p>
                    <button @click="closeErrorModal" class="px-6 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg w-full">Entendido</button>
                </div>
            </div>

        </div>
    </div>
    <footer >
        <WelcomeFooter />

         </footer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from "vue-router";
import * as AuthServices from '@/modules/auth/services/authServices';
import { isAxiosError } from 'axios';
import { useAuthStore } from '@/store/auth';
const router = useRouter(); // Descomentar si realmente se usa vue-router

// ----------------------------------------------------
// --- Variables de Estado del Profesional (Del Código Original) ---
// ----------------------------------------------------
const professionalData = ref<AuthServices.UserProfileData | null>(null); // Declaración para TypeScript

const loadingProfile = ref(true);

// --- FUNCIÓN TYPE GUARD (Ahora usa el alias del módulo) ---
const isProfessionalProfile = (data: AuthServices.UserProfileData): data is AuthServices.ProfessionalProfile => {
    // Verificación segura: comprueba si el campo 'link_code' existe en el objeto.
    return (data as AuthServices.ProfessionalProfile).link_code !== undefined;
};

// --- FUNCIÓN TYPE GUARD (Para el perfil de paciente) ---
const isPatientProfile = (data: AuthServices.UserProfileData): data is AuthServices.PatientProfile => {
    // Verificación segura: si tiene 'alias' y no tiene 'link_code', es un paciente.
    return (data as AuthServices.PatientProfile).alias !== undefined && !isProfessionalProfile(data);
};


const linkCode = ref('');
const dailyCodeChanges = ref(0);
const showCodeModal = ref(false);
const maxDailyChanges = 3;
const showSuccessUpdateModal = ref(false);
const newGeneratedCode = ref('');

// Lógica COMPUTED para determinar la BIENVENIDA según género
const professionalName = computed(() => {
    if (!professionalData.value) return 'Cargando...';

    // Accede a los campos de forma segura
    return `${professionalData.value.name} ${professionalData.value.paternal_last_name}`;
});

const salutation = computed(() => {
    if (!professionalData.value) return 'Bienvenido,';

    // Usamos el type guard para saber qué campo de género usar (sex o gender)
    if (isProfessionalProfile(professionalData.value)) {
        const gender = professionalData.value.sex.toLowerCase();
        return gender === 'female' ? 'Bienvenida,' : 'Bienvenido,';
    }
    // Si no es Professional (es Patient o superuser), usamos el campo gender del paciente o un default.
    // Asumimos que si no es profesional, debe ser un paciente que usa 'gender'.
    else if (isPatientProfile(professionalData.value)) {
        const gender = professionalData.value.gender.toLowerCase();
        return gender === 'female' ? 'Bienvenida,' : 'Bienvenido,';
    }

    return 'Bienvenido,';
});

// Función para carga de datos del backend
async function loadProfessionalData() {
    const authStore = useAuthStore();

    if (!authStore.authToken){
        console.error('No hay token de autenticación. Redirigiendo a login.');
        router.push({ name: 'login' });
        return;
    }

    try {
        // Llamada unificada a la API
        const response = await AuthServices.fetchUserProfile();

        professionalData.value = response.data;

        // ----------------------------------------------------
        // LÓGICA DE ASIGNACIÓN CONDICIONAL
        // ----------------------------------------------------
        if (isProfessionalProfile(response.data)) {
            // Si es un perfil de profesional, asignamos el link code real
            linkCode.value = response.data.link_code;
        } else {
            // Si el paciente accede a la vista de profesional, limpiamos el link code
            // y lo redirigimos si es necesario (el Navigation Guard debería prevenir esto).
            linkCode.value = '';
            // Si quieres redirigir a los pacientes a su propia vista:
            // router.push({ name: 'home-patient' });
        }

    } catch (error: unknown) {
        if (isAxiosError(error) && error.response && error.response.status === 401) {
            console.error('Token expirado. Forzando logout.');
            authStore.logout(); // Forzar el cierre de sesión y limpieza de tokens
            router.push({ name: 'login' });
        }
        console.error('Error al cargar datos del perfil:', error);
    } finally {
        loadingProfile.value = false;
    }
}


// ----------------------------------------------------
// --- Lógica del Código de Enlace (Del Código Original) ---
// ----------------------------------------------------

function openConfirmationModal() {
    showCodeModal.value = true;
}

async function confirmCodeGeneration() {
    showCodeModal.value = false; // Cerrar modal de confirmación

    // 1. CHEQUEO DEL LÍMITE DIARIO (se mantiene como simulación en el frontend)
    if (dailyCodeChanges.value >= maxDailyChanges) {
        // El botón debería estar deshabilitado, pero comprobamos de nuevo
        return;
    }

    // 2. LLAMADA REAL A LA API
    try {
        // En un escenario real, aquí podrías llamar a un endpoint para
        // obtener el contador de cambios de la DB para hacer esta verificación

        const response = await AuthServices.regenerateLinkCode();

        // 3. ACTUALIZAR ESTADO LOCAL
        if (response.status === 200) {
            const newCode = response.data.new_link_code;

            // Asignar el nuevo código al campo principal
            linkCode.value = newCode;

            // Incrementar el contador diario (Simulación, debe ser del backend en prod.)
            dailyCodeChanges.value++;

            // Asignar el código a la variable del modal de éxito
            newGeneratedCode.value = newCode;

            // Mostrar el modal de éxito
            showSuccessUpdateModal.value = true;
        }

    } catch (error: unknown) {
        if (isAxiosError(error) && error.response && error.response.status === 403) {
             errorMessage.value = 'No tienes permiso para realizar esta acción.';
        } else {
             errorMessage.value = 'Error al generar el código. Inténtelo de nuevo.';
        }
        showErrorModal.value = true;
        console.error('Error al generar código:', error);
    }
}


// ----------------------------------------------------
// --- Lógica de Seguridad (Fusionada) ---
// ----------------------------------------------------

// Variables para controlar los modales de seguridad
const activeSecurityModal = ref<string | null>(null);
const showSuccessModal = ref(false);
const showDeleteSuccessModal = ref(false);
const showErrorModal = ref(false);

// Variables para los formularios y mensajes de seguridad
const successTitle = ref("");
const successMessage = ref("");
const errorMessage = ref("");

// Variables para el flujo de cambio de email
const emailStep = ref(1); // 1: Pedir datos, 2: Verificar código
const currentPasswordEmail = ref(""); // Contraseña actual para el flujo de correo
const newEmail = ref("");
const verificationCode = ref(""); // Código que el usuario ingresa
const verificationError = ref<string | null>(null); // Error específico para la verificación
const emailError = ref<string | null>(null);

// Seguridad de reenvío/verificación de código
const resendAttempts = ref(0);
const maxResendAttempts = 3; // Máximo 3 reenvíos permitidos (cambiado a 3 para ser más estricto)
const verificationAttempts = ref(0);
const maxVerificationAttempts = 3; // Máximo 3 intentos de verificación fallidos
const isCodeInvalidated = ref(false); // Bandera para invalidación por intentos o expiración
const codeSentTime = ref<number | null>(null); // Timestamp del envío
const CODE_EXPIRY_MINUTES = 5; // Duración máxima de 5 minutos

// Contador y Timer para el email
const timeRemaining = ref(0); // Segundos restantes para el contador
let countdownTimer: number | null = null; // Variable para el setInterval

// Variables de cambio de contraseña
const currentPassword = ref("");
const newPassword = ref("");
const newPasswordConfirm = ref("");
const passwordError = ref<string | null>(null);

// Variables de eliminación de cuenta
const deletePassword = ref("");
const deletePasswordConfirm = ref("");
const deleteError = ref<string | null>(null);

// Computed para mostrar el estado del botón de reenvío
const canResendCode = computed(() => {
    // Si ya tiene el código invalidado O ya usó los 3 reenvíos
    return resendAttempts.value < maxResendAttempts && !isCodeInvalidated.value;
});

// Computed para el formato de tiempo (M:SS)
const formattedTime = computed(() => {
    const minutes = Math.floor(timeRemaining.value / 60);
    const seconds = timeRemaining.value % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
});

// --- FUNCIONES DE MODAL DE SEGURIDAD ---

// Función para abrir el modal correcto
function openSecurityModal(modalName: string) {
    activeSecurityModal.value = modalName;
    // Limpiar errores específicos y campos al abrir
    deleteError.value = null;
    passwordError.value = null;
    emailError.value = null;
    currentPassword.value = "";
    newPassword.value = "";
    newPasswordConfirm.value = "";
    deletePassword.value = "";
    deletePasswordConfirm.value = "";
    resetEmailFlow(); // Asegura que el flujo de email se reinicie
}

// Función para cerrar cualquier modal de seguridad y limpiar
function closeSecurityModal() {
    activeSecurityModal.value = null;
    resetEmailFlow(); // Limpieza específica del flujo de correo
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
// --- LÓGICA DE GESTIÓN DE CUENTA ---
// ----------------------------------------------------

// Lógica de TIMER para el flujo de email
function startCountdown() {
    // Iniciar con 5 minutos (300 segundos)
    timeRemaining.value = CODE_EXPIRY_MINUTES * 60;
    if (countdownTimer) clearInterval(countdownTimer);

    countdownTimer = setInterval(() => {
        if (timeRemaining.value > 0) {
            timeRemaining.value--;
        } else {
            // El tiempo ha expirado, invalidar el código
            clearInterval(countdownTimer as number);
            countdownTimer = null;
            isCodeInvalidated.value = true;
            verificationError.value = "El código de verificación ha expirado. Por favor, cancela y solicita uno nuevo."
        }
    }, 1000) as unknown as number;
}

// Función para reiniciar el flujo completo del email
function resetEmailFlow() {
    // Detener el contador primero
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
    newEmail.value = "";
    verificationCode.value = "";
    emailError.value = null;
    verificationError.value = null;
}

// Pre-verificación para el reenvío del código (solo aplica si estamos en el paso 2)
function resendCodeWithCheck() {
    if (emailStep.value === 2) {
        // Asegurarse de que las credenciales originales se mantienen
        if (!currentPasswordEmail.value || !newEmail.value) {
             emailError.value = "Error al reenviar. Cierra el modal y reinicia el proceso.";
             return;
        }
        sendVerificationCode();
    }
}

// Lógica para enviar el código de verificación
async function sendVerificationCode() {
    if (!currentPasswordEmail.value || !newEmail.value) {
        emailError.value = "Por favor, completa la contraseña y el nuevo correo.";
        return;
    }

    if (isCodeInvalidated.value) {
        emailError.value = "El código anterior fue invalidado. Cancela y reinicia el proceso.";
        return;
    }

    // Comprobación de límite de reenvío (solo si ya estamos en el paso 2 y es un reenvío)
    if (emailStep.value === 2 && resendAttempts.value >= maxResendAttempts) {
        emailError.value = `Has excedido el límite de ${maxResendAttempts} reenvíos. Reinicia el proceso.`;
        return;
    }

    emailError.value = null;

    try {
        // --- SIMULACIÓN DE API call para enviar código ---
        if (currentPasswordEmail.value === "error") {
            throw new Error("Contraseña actual incorrecta.");
        }
        // Simulación: Error de correo ya en uso (ej. si el correo es 'test@inuse.com')
        if (newEmail.value === "test@inuse.com") {
             throw new Error("El nuevo correo ya está registrado en la plataforma.");
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
        verificationError.value = "El código de verificación ha expirado. Por favor, solicita uno nuevo.";
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

        // Simular código incorrecto (el código correcto es "123456")
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
        closeSecurityModal();
        successTitle.value = "Correo actualizado";
        successMessage.value = `Tu correo electrónico ha sido actualizado a ${newEmail.value} con éxito.`;
        showSuccessModal.value = true;
        resetEmailFlow(); // Reiniciar todas las variables
    } catch (err: unknown) {
        const error = err as Error;

        // Manejar el error específico de intentos agotados o código incorrecto
        verificationError.value = error.message || "La verificación falló. Revisa tu código.";
    }
}


// Cambiar contraseña
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
    // Regex de seguridad (8-32, mayúscula, número, caracter especial)
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$/;
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

        closeSecurityModal();
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

// Borrar cuenta
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
        //borrar cuenta, eliminar datos del local storage - cerrar modal y redirigir a login


        closeSecurityModal();
        showDeleteSuccessModal.value = true;
    } catch (err: unknown) {
        console.error(err);
        const error = err as Error;
        errorMessage.value = error.message || "Hubo un problema al eliminar la cuenta. Por favor, inténtalo de nuevo.";
        showErrorModal.value = true;
    }
}

// Borrar cuenta y redirigir
function closeDeleteSuccessModal() {
    showDeleteSuccessModal.value = false;
    // Simulación de cierre de sesión y redirección
    localStorage.removeItem('authToken');
    localStorage.removeItem('userProfile');
    router.push('/login');
}

// Ciclo de vida para cargar los datos al inicio
onMounted(() => {
    loadProfessionalData();
});
</script>
