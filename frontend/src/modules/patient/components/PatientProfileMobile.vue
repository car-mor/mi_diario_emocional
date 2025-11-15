<template>
    <div class="flex h-screen">
        <!-- Área principal central -->
        <main class="dark:bg-gray-800 flex-1 flex flex-col overflow-hidden">

            <!-- Avatar -->
            <div class="mt-13 flex flex-col items-center text-center">
                <div class="relative w-40 h-40">
                    <div
                        v-if="loading"
                        class="w-full h-full rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse"
                    ></div>

                    <img
                        v-else
                        :src="avatarUrl || 'http://localhost:8000/static/images/avatar-icon.png'"
                        alt="User avatar"
                        class="w-40 h-40 rounded-xl object-cover cursor-pointer hover:opacity-80 transition-opacity"
                        @click="clickAvatarInput"
                        @error="handleImageError"
                    />

                    <button
                        v-if="hasCustomAvatar"
                        @click="removeAvatar"
                        class="absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center transition-colors shadow-lg"
                        title="Eliminar foto"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <input
                    type="file"
                    ref="avatarInput"
                    @change="handleAvatarChange"
                    accept="image/*"
                    class="hidden"
                />

                <h2 class="mt-3 text-lg font-semibold text-gray-800 dark:text-gray-200">
                    {{ userAlias }}
                </h2>
                <p class="text-sm text-gray-500">{{ userEmail }}</p>
                <p class="text-xs text-gray-500 mt-1">
                    {{ hasCustomAvatar ? 'Toca la imagen para cambiar la foto' : 'Toca la imagen para agregar una foto' }}
                </p>
            </div>

            <!-- Descripción -->
            <div @dblclick="isEditingDescription = true" class="group relative cursor-pointer mx-6">
                <IconEdit
                    v-if="!isEditingDescription"
                    class="w-4 h-4 text-gray-400 absolute top-0 right-0 mt-1 mr-1 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                    @click="isEditingDescription = true"
                />
                <p v-if="!isEditingDescription" class="text-center mt-4 text-sm text-gray-600 dark:text-gray-400">
                    {{ userDescription }}
                </p>

                <div v-else class="mt-4">
                    <textarea
                        v-model="userDescription"
                        class="w-full p-2 border rounded resize-none text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        rows="4"
                    ></textarea>
                    <p v-if="descriptionError" class="text-red-500 text-xs mt-1">{{ descriptionError }}</p>
                    <div class="flex justify-end space-x-2 mt-2">
                        <button
                            @click="cancelEdit"
                            class="text-xs text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-1 px-3 rounded-lg transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            @click="saveDescription"
                            class="text-xs bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-1 px-3 rounded-lg transition-colors text-center"
                        >
                            Guardar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Botones -->
            <div class="mt-6 flex flex-col gap-3 items-center">
                <router-link
                    to="/account-settings"
                    class="w-60 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 inline-block text-center"
                >
                    Configurar cuenta
                </router-link>

                <button
                    @click="handleLogout"
                    class="w-60 text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                    Cerrar sesión
                </button>
            </div>

            <!-- ✅ MODAL DE ERROR/WARNING -->
            <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="fixed inset-0 bg-black bg-opacity-50" @click="closeErrorModal"></div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-md w-full text-center relative z-10 mx-4">
                    <div class="flex justify-center mb-4">
                        <div class="bg-orange-500 p-3 rounded-full inline-flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                            </svg>
                        </div>
                    </div>
                    <h3 class="text-xl font-bold mb-3 dark:text-white">{{ errorTitle }}</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ errorMessage }}</p>
                    <button
                        @click="closeErrorModal"
                        class="px-6 py-2 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg w-full transition-colors"
                    >
                        Entendido
                    </button>
                </div>
            </div>

            <!-- Modal de confirmación para eliminar foto -->
            <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="fixed inset-0" @click="closeDeleteModal"></div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">¿Eliminar foto de perfil?</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">
                        Esta acción eliminará tu foto personalizada y se mostrará la imagen predeterminada.
                    </p>
                    <div class="flex justify-center mb-6">
                        <div class="bg-red-500 p-3 rounded-full inline-flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                        </div>
                    </div>
                    <div class="flex gap-3">
                        <button
                            @click="closeDeleteModal"
                            class="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            @click="confirmDeleteAvatar"
                            class="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors"
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Modal de éxito -->
            <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="fixed inset-0" @click="closeSuccessModal"></div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">{{ successTitle }}</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-6">{{ successMessage }}</p>
                    <div class="flex justify-center mb-4">
                        <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                    </div>
                    <button
                        @click="closeSuccessModal"
                        class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full transition-colors"
                    >
                        Entendido
                    </button>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { storeToRefs } from 'pinia';
import * as AuthServices from '@/modules/auth/services/authServices';
import { IconEdit } from '@tabler/icons-vue';
import { type PatientUpdatePayload } from '@/modules/auth/services/authServices';

const router = useRouter();
const authStore = useAuthStore();
// Obtenemos el estado reactivo directamente del store
const { userProfile, loading } = storeToRefs(authStore);

// const patientData = ref<AuthServices.UserProfileData | null>(null);
// const loadingProfile = ref(true);
const isPatientProfile = (data: AuthServices.UserProfileData): data is AuthServices.PatientProfile => {
    return (data as AuthServices.PatientProfile).alias !== undefined;
};

// const userAlias = computed(() => {
//     if (!patientData.value) return 'Cargando...';
//     if (isPatientProfile(patientData.value)) {
//         return patientData.value.alias;
//     }
//     return patientData.value.name;
// });
const userAlias = computed(() => {
    if (!userProfile.value) return 'Cargando...';
    if (isPatientProfile(userProfile.value)) {
        return userProfile.value.alias;
    }
    return userProfile.value.name;
});

const userEmail = computed(() => {
    return userProfile.value ? userProfile.value.email : 'Cargando...';
});

// Constantes para descripción (inicializadas desde el store)
const userDescription = ref((userProfile.value as AuthServices.PatientProfile)?.description || '');
const originalDescription = ref("");
const isEditingDescription = ref(false);
const descriptionError = ref<string | null>(null);

// Constantes para foto
const avatarInput = ref<HTMLInputElement | null>(null);
// const avatarUrl = ref<string | null>(null);

// Constantes para modales
const showDeleteModal = ref(false);
const showSuccessModal = ref(false);
const successTitle = ref('');
const successMessage = ref('');
const showErrorModal = ref(false);
const errorTitle = ref('');
const errorMessage = ref('');

function showError(title: string, message: string) {
    errorTitle.value = title;
    errorMessage.value = message;
    showErrorModal.value = true;
}

function closeErrorModal() {
    showErrorModal.value = false;
}

const avatarUrl = computed(() => (userProfile.value as AuthServices.PatientProfile)?.profile_picture_url);

const hasCustomAvatar = computed(() => {
    return avatarUrl.value?.includes('/media/') || false;
});
function clickAvatarInput() {
    if (avatarInput.value) {
        avatarInput.value.click();
    }
}

function handleImageError(event: Event) {
    console.error('❌ Error al cargar imagen:', avatarUrl.value);
    const target = event.target as HTMLImageElement;
    target.src = 'http://localhost:8000/static/images/avatar-icon.png';
}

async function handleAvatarChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (!file) return;

    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validImageTypes.includes(file.type)) {
        showError(
            'Formato no válido',
            'El archivo seleccionado no es una imagen válida. Por favor, selecciona un archivo en formato JPG, PNG, GIF o WEBP.'
        );
        target.value = '';
        return;
    }

    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
        showError(
            'Archivo muy grande',
            `La imagen seleccionada pesa ${fileSizeMB} MB, pero el límite máximo es de 50 MB. Por favor, comprime la imagen o selecciona una más pequeña.`
        );
        target.value = '';
        return;
    }

    try {
        console.log('📤 Subiendo imagen:', file.name, `(${(file.size / (1024 * 1024)).toFixed(2)} MB)`);

        const formData = new FormData();
        formData.append('profile_picture', file);

        const response = await AuthServices.updatePatientProfile(formData);

        // if (response.data.profile_picture_url) {
        //     avatarUrl.value = response.data.profile_picture_url;
        // } else if (response.data.profile_picture) {
        //     avatarUrl.value = response.data.profile_picture;
        // }
        authStore.updateUserProfile({ profile_picture_url: response.data.profile_picture_url });
        successTitle.value = '¡Foto actualizada!';
        successMessage.value = 'Tu foto de perfil ha sido actualizada correctamente.';
        showSuccessModal.value = true;

    } catch (error) {
        console.error('❌ Error al subir avatar:', error);
        showError(
            'Error al subir',
            'Hubo un problema al subir tu imagen. Por favor, intenta nuevamente o selecciona otra imagen.'
        );
    } finally {
        if (target) {
            target.value = '';
        }
    }
}

async function saveDescription() {
    if (!validateDescription(userDescription.value)) {
        return;
    }

    try {
        const payload: PatientUpdatePayload = { description: userDescription.value };
        await AuthServices.updatePatientProfile(payload);

        authStore.updateUserProfile({ description: userDescription.value });

        originalDescription.value = userDescription.value;
        isEditingDescription.value = false;

        successTitle.value = '¡Actualizado!';
        successMessage.value = 'Tu descripción ha sido guardada correctamente.';
        showSuccessModal.value = true;

    } catch (error) {
        console.error('Error al guardar descripción:', error);
    }
}

function validateDescription(text: string): boolean {
    const cleanText = text.trim();
    if (cleanText.length === 0) {
        descriptionError.value = "La descripción no puede estar vacía.";
        return false;
    }
    if (cleanText.length < 3) {
        descriptionError.value = "Mínimo 3 caracteres.";
        return false;
    }
    if (cleanText.length > 150) {
        descriptionError.value = "Máximo 150 caracteres.";
        return false;
    }
    descriptionError.value = null;
    return true;
}

function cancelEdit() {
    userDescription.value = originalDescription.value;
    isEditingDescription.value = false;
    descriptionError.value = null;
}

function removeAvatar() {
    showDeleteModal.value = true;
}

function closeDeleteModal() {
    showDeleteModal.value = false;
}

async function confirmDeleteAvatar() {
    try {
        console.log('🗑️ Eliminando avatar...');

        const formData = new FormData();
        formData.append('delete_picture', 'true');

        const response = await AuthServices.updatePatientProfile(formData);

        // if (response.data.profile_picture_url) {
        //     avatarUrl.value = response.data.profile_picture_url;
        // } else if (response.data.profile_picture) {
        //     avatarUrl.value = response.data.profile_picture;
        // }
        authStore.updateUserProfile({ profile_picture_url: response.data.profile_picture_url });

        successTitle.value = '¡Foto eliminada!';
        successMessage.value = 'Tu foto de perfil ha sido eliminada correctamente.';
        showSuccessModal.value = true;
        closeDeleteModal();

    } catch (error: unknown) {
        console.error('❌ Error al eliminar avatar:', error);

        if (error && typeof error === 'object' && 'response' in error) {
            const axiosError = error as { response?: { data: unknown; status: number } };
            if (axiosError.response) {
                console.error('❌ Respuesta del servidor:', axiosError.response.data);
                console.error('❌ Status:', axiosError.response.status);
            }
        }

        showError(
            'Error al eliminar',
            'Hubo un problema al eliminar tu foto. Por favor, intenta nuevamente.'
        );
    }
}

function closeSuccessModal() {
    showSuccessModal.value = false;
}

const handleLogout = async () => {
    loading.value = true;

    try {
        await authStore.logout();
        router.push({ name: 'login' });
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        router.push({ name: 'login' });
    } finally {
        loading.value = false;
    }
};

// async function loadPatientData() {
//     loadingProfile.value = true;

//     if (!authStore.authToken) {
//         router.push({ name: 'login' });
//         loadingProfile.value = false;
//         return;
//     }

//     try {
//         const response = await AuthServices.fetchUserProfile();
//         const patientProfile = response.data as AuthServices.PatientProfile;

//         patientData.value = patientProfile;
//         userDescription.value = patientProfile.description || 'Añade una breve descripción sobre ti...';
//         originalDescription.value = userDescription.value;
//         avatarUrl.value = patientProfile.profile_picture;

//     } catch (error) {
//         console.error("Falló la carga del perfil de usuario:", error);
//     } finally {
//         loadingProfile.value = false;
//     }
// }

// onMounted(() => {
//     loadPatientData();

//     return () => {
//         if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
//             URL.revokeObjectURL(avatarUrl.value);
//         }
//     };
// });
</script>
