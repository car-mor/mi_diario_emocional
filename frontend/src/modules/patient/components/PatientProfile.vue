<template>
    <aside
        class="hidden lg:flex w-90 bg-white border-l border-gray-200 dark:bg-gray-900 dark:border-gray-800 p-6 flex-col transition-colors"
    >
        <div class="flex flex-col items-center text-center">
            <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                Perfil del usuario
            </h2>
        </div>

        <div class="mt-13 flex flex-col items-center text-center relative group">
            <!-- Estado de carga -->
            <div class="relative w-40 h-40">
                <div
                    v-if="loading"
                    class="w-full h-full rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse"
                ></div>

                <!-- Imagen del avatar -->
                <img
                    v-else
                    :src="avatarUrl || '/images/avatar-icon.png'"
                    alt="User avatar"
                    class="w-40 h-40 rounded-xl object-cover cursor-pointer hover:opacity-80 transition-opacity"
                    @click="clickAvatarInput"
                    @error="handleImageError"
                />

                <!-- Botón para eliminar -->
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
          <h2 class="mt-4 text-xl font-bold text-gray-900 dark:text-white">
            {{ userFullName }}
          </h2>
            <h2 class="mt-3 text-lg font-semibold text-gray-800 dark:text-gray-200">
                @{{ userAlias }}
            </h2>
            <p class="text-sm text-gray-500">{{ userEmail }}</p>

            <p class="text-sm text-gray-500 mt-2">
                {{ hasCustomAvatar ? 'Haz clic en la foto para cambiarla' : 'Haz clic en la foto para agregar una' }}
            </p>
        </div>

        <!-- Descripción -->
<div class="mt-4">
  <!-- Modo visualización -->
  <div v-if="!isEditingDescription">
    <!-- Si tiene descripción -->
    <div v-if="userDescription.trim()" class="relative">
      <div class="flex items-start justify-between gap-3 mb-3">
        <p class="flex-1 text-center text-sm text-gray-600 dark:text-gray-400">
          {{ userDescription }}
        </p>
        <button
          @click="startEditing"
          class="flex-shrink-0 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Editar descripción"
        >
          <IconEdit class="w-5 h-5 text-gray-500 dark:text-gray-400" />
        </button>
      </div>
    </div>

    <!-- Si NO tiene descripción (estado vacío) -->
    <div v-else class="text-center">
      <p class="text-sm text-gray-500 dark:text-gray-400 italic mb-3">
        Aún no has agregado una descripción
      </p>
      <button
        @click="startEditing"
        class="w-full flex items-center justify-center gap-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-2 px-4 rounded-lg transition-colors"
      >
        <IconEdit class="w-4 h-4" />
        <span class="text-sm">Agregar descripción</span>
      </button>
    </div>
  </div>

  <!-- Modo edición -->
  <div v-else>
    <textarea
      ref="descriptionTextarea"
      v-model="userDescription"
      class="w-full p-2 border rounded-lg resize-none text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-[#7DBFF8] focus:border-transparent"
      rows="4"
      placeholder="Escribe algo sobre ti..."
    ></textarea>
    <p v-if="descriptionError" class="text-red-500 text-xs mt-1">{{ descriptionError }}</p>
    <div class="flex gap-2 mt-2">
      <button
        @click="cancelEdit"
        class="flex-1 text-xs text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-2 px-3 rounded-lg transition-colors"
      >
        Cancelar
      </button>
      <button
        @click="saveDescription"
        :disabled="isSaving"
        class="flex-1 text-xs bg-[#7DBFF8] hover:bg-[#3457B2] disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-2 px-3 rounded-lg transition-colors text-center"
      >
        {{ isSaving ? 'Guardando...' : 'Guardar' }}
      </button>
    </div>
  </div>
</div>

        <div class="mt-6 flex flex-col gap-3">
            <router-link
                to="/account-settings"
                class="w-full bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 inline-block text-center"
            >
                Configurar cuenta
            </router-link>
            <button
                @click.prevent="handleLogout"
                class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
                Cerrar sesión
            </button>
        </div>

        <!-- ✅ MODAL DE ERROR/WARNING -->
        <div v-if="showErrorModal" class="fixed inset-0 flex items-center justify-center z-50">
            <div class="fixed inset-0" @click="closeErrorModal"></div>
            <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-md w-full text-center relative z-10">
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

        <!-- MODAL DE CONFIRMACIÓN DE ELIMINACIÓN -->
        <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center z-50">
            <div class="fixed inset-0" @click="closeDeleteModal"></div>
            <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10">
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

        <!-- MODAL DE ÉXITO -->
        <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
            <div class="fixed inset-0" @click="closeSuccessModal"></div>
            <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center relative z-10">
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
    </aside>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { storeToRefs } from 'pinia';
import * as AuthServices from '@/modules/auth/services/authServices';
import { IconEdit } from '@tabler/icons-vue';
import { type PatientUpdatePayload } from '@/modules/auth/services/authServices';
const router = useRouter();
const authStore = useAuthStore();

const isPatientProfile = (data: AuthServices.UserProfileData): data is AuthServices.PatientProfile => {
    // Si tiene la propiedad 'alias' y no tiene 'link_code' (lo que define a un Profesional)
    return (data as AuthServices.PatientProfile).alias !== undefined;
};


const { userProfile, loading } = storeToRefs(authStore);

const userAlias = computed(() => {
    if (!userProfile.value) return 'Cargando...';

    if (isPatientProfile(userProfile.value)) {
        return userProfile.value.alias;
    }

    // Fallback: Si no es PatientProfile (ej. Superuser logueado en esta vista),
    // podemos mostrar el nombre completo.
    return userProfile.value.name;
});


const userEmail = computed(() => {
    // Si los datos están cargados, muestra el email
    return userProfile.value ? userProfile.value.email : 'Cargando...';
});

const userFullName = computed(() => {
    if (!userProfile.value) return 'Cargando...';

    // 1. Crea una lista con las partes del nombre
    const parts = [
        userProfile.value.name,
        userProfile.value.paternal_last_name,
        userProfile.value.maternal_last_name
    ];

    // 2. Filtra la lista para quitar valores "falsy" (null, undefined, '')
    // 3. Une las partes filtradas con un espacio
    return parts.filter(Boolean).join(' ');
});

//----------- constantes para el alias y descripción ---------------------
const userDescription = ref( (userProfile.value as AuthServices.PatientProfile)?.description || '');
const originalDescription = ref(""); // Para guardar la descripción original antes de editar
const isEditingDescription = ref(false);
const descriptionError = ref<string | null>(null);
const descriptionTextarea = ref<HTMLTextAreaElement | null>(null);
const isSaving = ref(false);
//-------------- constantes para la foto ------------------
const avatarInput = ref<HTMLInputElement | null>(null);
// const avatarUrl = ref<string | null>(null);
// Lee directamente del 'userProfile' del store. Ya no es una variable local.
const avatarUrl = computed(() => (userProfile.value as AuthServices.PatientProfile)?.profile_picture_url);

//-------------- constantes para modales ------------------
const showDeleteModal = ref(false);
const showSuccessModal = ref(false);
const successTitle = ref('');
const successMessage = ref('');
// Variables para el modal de error
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


// Computed para saber si el usuario tiene una foto personalizada
const hasCustomAvatar = computed(() => {
    return avatarUrl.value?.includes('/media/') || false;
});


function clickAvatarInput() {
    if (avatarInput.value) {
        avatarInput.value.click(); // Dispara el clic en el input de tipo file
    }
}
// Si la imagen falla (incluso la de DigitalOcean o la de Railway),
// usamos el fallback local de la carpeta /public.
function handleImageError(event: Event) {
  console.error('❌ Error al cargar imagen:', avatarUrl.value);
  const target = event.target as HTMLImageElement;
  target.src = '/images/avatar-icon.png'; // <-- Se elimina 'localhost:8000'
}

async function handleAvatarChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (!file) return;

    // Validación 1: Tipo de archivo
    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validImageTypes.includes(file.type)) {
        showError(
            'Formato no válido',
            'El archivo seleccionado no es una imagen válida. Por favor, selecciona un archivo en formato JPG, PNG, GIF o WEBP.'
        );
        target.value = '';
        return;
    }

    // Validación 2: Tamaño de archivo (50MB máximo)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
        const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
        showError(
            'Archivo muy grande',
            `La imagen seleccionada pesa ${fileSizeMB} MB, pero el límite máximo es de 50 MB. Por favor, comprime la imagen o selecciona una más pequeña.`
        );
        target.value = '';
        return;
    }

    // Si pasa todas las validaciones, proceder con la subida
    try {
        console.log('📤 Subiendo imagen:', file.name, `(${(file.size / (1024 * 1024)).toFixed(2)} MB)`);

        const formData = new FormData();
        formData.append('profile_picture', file);

        const response = await AuthServices.updatePatientProfile(formData);

        console.log('✅ Respuesta de actualización:', response.data);
        authStore.updateUserProfile({ profile_picture_url: response.data.profile_picture_url });
        // Mostrar modal de éxito
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



const handleLogout = async () => {
    loading.value = true;

    try {
        // La función logout de Pinia ya maneja la llamada al endpoint /api/logout/
        await authStore.logout();

        // Redirigir a la página de login
        router.push({ name: 'login' });

    } catch (error) {
        // Si hay un error de red o el servidor no responde (ej. 500)
        console.error('Error al cerrar sesión, forzando cierre local:', error);

        // Forzamos la redirección aunque el blacklisting del token haya fallado,
        // para garantizar que el usuario salga de la sesión local.
        router.push({ name: 'login' });

    } finally {
        loading.value = false;
    }
};
//-----------------------------------------------------------------------
//------------------- Funciones de Validación y Edición -----------------
//-----------------------------------------------------------------------

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

async function startEditing() {
  originalDescription.value = userDescription.value; // Guarda el valor actual por si cancela
  isEditingDescription.value = true;
  await nextTick();
  descriptionTextarea.value?.focus();
}

// ✅ Actualiza tu función saveDescription
async function saveDescription() {
    if (!validateDescription(userDescription.value)) {
        return;
    }

    isSaving.value = true; // ✅ Inicia loading

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
        showError(
            'Error al guardar',
            'Hubo un problema al guardar tu descripción. Por favor, intenta nuevamente.'
        );
    } finally {
        isSaving.value = false; // ✅ Termina loading
    }
}
function cancelEdit() {
    // Revertir a la última versión guardada
    userDescription.value = originalDescription.value;
    isEditingDescription.value = false;
    descriptionError.value = null;
}

//------------------- Funciones para avatar --------------------------




function removeAvatar() {
    showDeleteModal.value = true;
}

function closeDeleteModal() {
    showDeleteModal.value = false;
}

async function confirmDeleteAvatar() {
    try {
        console.log('🗑️ Eliminando avatar...');

        // ✅ Crear FormData con el flag de eliminación
        const formData = new FormData();
        formData.append('delete_picture', 'true');

        // DEBUG: Ver qué contiene el FormData antes de enviarlo
        console.log('📤 Contenido del FormData:');
        for (const pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        const response = await AuthServices.updatePatientProfile(formData);

        console.log('✅ Respuesta de eliminación:', response.data);
        authStore.updateUserProfile({ profile_picture_url: response.data.profile_picture_url });
        console.log('✅ Avatar eliminado, nueva URL:', avatarUrl.value);

        // Mostrar modal de éxito
        successTitle.value = '¡Foto eliminada!';
        successMessage.value = 'Tu foto de perfil ha sido eliminada correctamente.';
        showSuccessModal.value = true;
        closeDeleteModal();

    } catch (error: unknown) {
        console.error('❌ Error completo al eliminar avatar:', error);

        // ✅ Type guard para verificar si es un error de Axios
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
</script>
