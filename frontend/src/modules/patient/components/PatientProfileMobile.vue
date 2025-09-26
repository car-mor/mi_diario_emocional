<template>
    <div class="flex h-screen">

        <!-- Área principal central -->
        <main class="dark:bg-gray-800 flex-1 flex flex-col overflow-hidden">

            <!-- Avatar -->
            <div class="mt-13 flex flex-col items-center text-center">
                <div class="relative">
                    <img
                        :src="finalAvatarSrc"
                        alt="User avatar"
                        class="w-40 h-40 rounded-xl object-cover cursor-pointer hover:opacity-80 transition-opacity"
                        @click="clickAvatarInput"
                    />
                    <!-- Botón eliminar foto (solo se muestra si hay una foto personalizada) -->
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

            <!-- Botón Configurar cuenta -->
            <div class="mt-6 flex flex-col gap-3 items-center">
                <router-link
                    to="/account-settings"
                    class="w-60 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4 inline-block text-center"
                >
                    Configurar cuenta
                </router-link>

                <router-link
                    to="/"
                    class="w-60 sm:w-auto text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors inline-block"
                >
                    Cerrar sesión
                </router-link>
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
import { ref, computed, onMounted } from 'vue';
import { IconEdit } from '@tabler/icons-vue';

//----------- constantes para el perfil ---------------------
const userAlias = ref("Alias de María");
const userEmail = ref("maria@correo.com");

//----------- constantes para la descripción ----------------
const userDescription = ref("Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui. Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui."); 
const originalDescription = ref(""); // Para guardar la descripción original
const isEditingDescription = ref(false);
const descriptionError = ref<string | null>(null);

//-------------- constantes para la foto ------------------
const avatarInput = ref<HTMLInputElement | null>(null);
// Ruta relativa a la imagen por defecto en tu carpeta public
const defaultAvatar = '/images/avatar-icon.png'; 
const avatarUrl = ref<string | null>(null); // ejemplo: https://i.pravatar.cc/150?img=38

//-------------- constantes para modales ------------------
const showDeleteModal = ref(false);
const showSuccessModal = ref(false);
const successTitle = ref('');
const successMessage = ref('');

// Computed para determinar qué imagen mostrar
const finalAvatarSrc = computed(() => avatarUrl.value || defaultAvatar);

// Computed para saber si el usuario tiene una foto personalizada
const hasCustomAvatar = computed(() => avatarUrl.value !== null);

//-----------------------------------------------------------------------
//------------------- Funciones para editar descripción -----------------
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
        // AQUÍ VA LA LLAMADA AXIOS/FETCH AL BACKEND para guardar userDescription.value
        console.log("Guardando descripción:", userDescription.value);
        
        // Actualizar la descripción original
        originalDescription.value = userDescription.value;
        isEditingDescription.value = false;
        descriptionError.value = null;
        
        // Mostrar modal de éxito
        successTitle.value = '¡Descripción guardada!';
        successMessage.value = 'Tu descripción ha sido actualizada correctamente.';
        showSuccessModal.value = true;
    }
}

function cancelEdit() {
    // Revertir a la última versión guardada
    userDescription.value = originalDescription.value;
    isEditingDescription.value = false;
    descriptionError.value = null;
}

//-----------------------------------------------------------------------
//------------------- Funciones para editar foto -------------------------
//-----------------------------------------------------------------------

function handleAvatarChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        // Validar que sea una imagen
        if (!file.type.startsWith('image/')) {
            console.error('El archivo debe ser una imagen');
            return;
        }

        // Validar tamaño del archivo (ej: máximo 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB en bytes
        if (file.size > maxSize) {
            console.error('La imagen es demasiado grande. Máximo 5MB.');
            return;
        }

        // Limpiar URL anterior si existe
        if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(avatarUrl.value);
        }

        // Mostrar vista previa temporal al usuario
        avatarUrl.value = URL.createObjectURL(file);

        // AQUÍ deberías hacer la llamada al backend para subir el archivo
        uploadAvatar(file);
    }
}

function removeAvatar() {
    // Mostrar modal de confirmación
    showDeleteModal.value = true;
}

function closeDeleteModal() {
    showDeleteModal.value = false;
}

function confirmDeleteAvatar() {
    // Cerrar modal de confirmación
    showDeleteModal.value = false;
    
    // Limpiar URL blob si existe
    if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(avatarUrl.value);
    }
    
    // Resetear a null para usar la imagen por defecto
    avatarUrl.value = null;
    
    // AQUÍ harías la llamada al backend para eliminar la foto del servidor
    deleteAvatarFromServer();
    
    // Mostrar modal de éxito
    successTitle.value = '¡Foto eliminada!';
    successMessage.value = 'Tu foto de perfil ha sido eliminada correctamente. Ahora se muestra la imagen predeterminada.';
    showSuccessModal.value = true;
    
    console.log("Foto de perfil eliminada");
}

function closeSuccessModal() {
    showSuccessModal.value = false;
}

// También puedes mostrar modal de éxito después de subir una foto
function showUploadSuccess() {
    successTitle.value = '¡Foto actualizada!';
    successMessage.value = 'Tu foto de perfil ha sido actualizada correctamente.';
    showSuccessModal.value = true;
}

async function uploadAvatar(file: File) {
    try {
        // Ejemplo de subida de archivo
        const formData = new FormData();
        formData.append('avatar', file);

        // DESCOMENTA Y ADAPTA SEGÚN TU API
        /*
        const response = await fetch('/api/upload-avatar', {
            method: 'POST',
            body: formData,
            headers: {
                // Agregar headers de autenticación si es necesario
            }
        });

        if (response.ok) {
            const data = await response.json();
            // Limpiar URL temporal
            if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
                URL.revokeObjectURL(avatarUrl.value);
            }
            // Usar URL permanente del servidor
            avatarUrl.value = data.avatarUrl;
            
            // Mostrar modal de éxito
            showUploadSuccess();
        } else {
            throw new Error('Error al subir la imagen');
        }
        */

        console.log("Archivo listo para subir:", file.name);
        
        // Comentado para demo: showUploadSuccess();
    } catch (error) {
        console.error('Error al subir avatar:', error);
        // Revertir a imagen anterior o por defecto
        if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(avatarUrl.value);
        }
        avatarUrl.value = null;
    }
}

async function deleteAvatarFromServer() {
    try {
        // DESCOMENTA Y ADAPTA SEGÚN TU API
        /*
        const response = await fetch('/api/delete-avatar', {
            method: 'DELETE',
            headers: {
                // Agregar headers de autenticación si es necesario
            }
        });

        if (!response.ok) {
            throw new Error('Error al eliminar la imagen del servidor');
        }
        */

        console.log("Solicitud de eliminación enviada al servidor");
    } catch (error) {
        console.error('Error al eliminar avatar del servidor:', error);
        // Opcionalmente, podrías revertir el cambio local si falla la eliminación en el servidor
    }
}

function clickAvatarInput() {
    if (avatarInput.value) {
        avatarInput.value.click();
    }
}

// Cleanup cuando el componente se desmonte
onMounted(() => {
    // Guardar descripción original
    originalDescription.value = userDescription.value;
    
    // Cleanup function que se ejecuta cuando el componente se desmonta
    return () => {
        if (avatarUrl.value && avatarUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(avatarUrl.value);
        }
    };
});
</script>