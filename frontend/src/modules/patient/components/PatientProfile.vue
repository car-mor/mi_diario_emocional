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
            <div class="relative">
                <img
                    :src="finalAvatarSrc"
                    alt="User avatar"
                    class="w-40 h-40 rounded-xl object-cover cursor-pointer hover:opacity-80 transition-opacity"
                    @click="clickAvatarInput"
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
            
            <p class="text-sm text-gray-500 mt-2">
                {{ hasCustomAvatar ? 'Haz clic para cambiar la foto' : 'Haz clic para agregar una foto' }}
            </p>
        </div>

        <div @dblclick="isEditingDescription = true" class="group relative cursor-pointer">
            <IconEdit
                v-if="!isEditingDescription"
                class="w-4 h-4 text-gray-400 absolute top-0 right-0 mt-1 mr-1 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                @click="isEditingDescription = true"
            />
            <p v-if="!isEditingDescription" class="mt-4 text-sm text-gray-600 dark:text-gray-400 text-center">
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
                    <button @click="cancelEdit" class="text-xs text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-1 px-3 rounded-lg transition-colors">Cancelar</button>
                    <button @click="saveDescription" class="text-xs bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-1 px-3 rounded-lg transition-colors text-center">Guardar</button>
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
            <router-link
                to="/"
                class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
                Cerrar sesión
            </router-link>
        </div>

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
import { ref, computed, onMounted } from 'vue';
import { IconEdit } from '@tabler/icons-vue';

// --- NUEVAS VARIABLES PARA ALIAS Y CORREO ---
const userAlias = ref(''); // Se llena desde el backend
const userEmail = ref(''); // Se llena desde el backend
// --- FIN NUEVAS VARIABLES ---

//----------- constantes para el alias y descripción ---------------------
const userDescription = ref(""); 
const originalDescription = ref(""); // Para guardar la descripción original antes de editar
const isEditingDescription = ref(false);
const descriptionError = ref<string | null>(null);

//-------------- constantes para la foto ------------------
const avatarInput = ref<HTMLInputElement | null>(null);
const defaultAvatar = '/src/assets/images/avatar-icon.png'; 
const avatarUrl = ref<string | null>(null); 

//-------------- constantes para modales ------------------
const showDeleteModal = ref(false);
const showSuccessModal = ref(false);
const successTitle = ref('');
const successMessage = ref('');

// Computed para determinar qué imagen mostrar
const finalAvatarSrc = computed(() => avatarUrl.value || defaultAvatar);

// Computed para saber si el usuario tiene una foto personalizada
const hasCustomAvatar = computed(() => avatarUrl.value !== null && avatarUrl.value !== defaultAvatar);

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

function saveDescription() {
    if (validateDescription(userDescription.value)) {
        // LLAMADA AXIOS/FETCH AL BACKEND para guardar userDescription.value
        console.log("Guardando descripción:", userDescription.value);
        originalDescription.value = userDescription.value;
        isEditingDescription.value = false;
    }
}

function cancelEdit() {
    // Revertir a la última versión guardada
    userDescription.value = originalDescription.value;
    isEditingDescription.value = false;
    descriptionError.value = null;
}

//------------------- Funciones para avatar --------------------------

function handleAvatarChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        if (!file.type.startsWith('image/')) {
            console.error('El archivo debe ser una imagen');
            return;
        }
        const maxSize = 5 * 1024 * 1024; // 5MB en bytes
        if (file.size > maxSize) {
            console.error('La imagen es demasiado grande. Máximo 5MB.');
            return;
        }

        if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(avatarUrl.value);
        }

        avatarUrl.value = URL.createObjectURL(file);
        uploadAvatar(file);
    }
}

function showUploadSuccess() {
    successTitle.value = '¡Foto actualizada!';
    successMessage.value = 'Tu foto de perfil ha sido actualizada correctamente.';
    showSuccessModal.value = true;
}

function removeAvatar() {
    showDeleteModal.value = true;
}

function closeDeleteModal() {
    showDeleteModal.value = false;
}

function confirmDeleteAvatar() {
    showDeleteModal.value = false;
    
    if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(avatarUrl.value);
    }
    
    avatarUrl.value = null;
    deleteAvatarFromServer();
    
    successTitle.value = '¡Foto eliminada!';
    successMessage.value = 'Tu foto de perfil ha sido eliminada correctamente. Ahora se muestra la imagen predeterminada.';
    showSuccessModal.value = true;
    console.log("Foto de perfil eliminada");
}

function closeSuccessModal() {
    showSuccessModal.value = false;
}

async function uploadAvatar(file: File) {
    // Lógica para subir el archivo al backend
    console.log("Simulación: Subiendo archivo al servidor...");
    // Simular éxito y asignar la URL permanente si tuvieras una
    // avatarUrl.value = data.avatarUrl; 
    showUploadSuccess();
}

async function deleteAvatarFromServer() {
    // Lógica para notificar al backend que elimine la foto
    console.log("Simulación: Solicitud de eliminación enviada al servidor.");
}

function clickAvatarInput() {
    if (avatarInput.value) {
        avatarInput.value.click();
    }
}

// ----------------------------------------------------
// Lógica de Carga Inicial (Backend)
// ----------------------------------------------------

async function loadUserProfileData() {
    try {
        // Simulación de datos recibidos del backend
        await new Promise(resolve => setTimeout(resolve, 300));
        
        const dataFromBackend = {
            alias: 'Alias de María',
            email: 'maria@correo.com',
            description: 'Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui.',
            // El backend envía la URL si existe, o null si no hay foto personalizada
            avatar_url: null as string | null, 
        };

        // Asignar los valores a las variables reactivas
        userAlias.value = dataFromBackend.alias;
        userEmail.value = dataFromBackend.email;
        userDescription.value = dataFromBackend.description;
        originalDescription.value = dataFromBackend.description; // Establece el valor de reversión
        
        // CORRECCIÓN de la asignación del avatar:
        // Asignamos el valor del backend. Si es null, el computed se encarga del default.
        avatarUrl.value = dataFromBackend.avatar_url; 
        
    } catch (error) {
        console.error('Error al cargar datos del perfil:', error);
    }
}

// Ciclo de vida
onMounted(() => {
    loadUserProfileData();
    
    // Cleanup function que se ejecuta cuando el componente se desmonta
    return () => {
        if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(avatarUrl.value);
        }
    };
});
</script>