<template>
    <div class="flex h-screen">
        <Sidebar />
        
        <main class="flex-1 flex flex-col overflow-hidden">
            <StreakAndTitle title="No estas vinculado a algún profesional de la salud mental 😢" :streakCount="2" />
            
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto flex flex-col items-center justify-center">
                
                <div class="p-4 flex flex-col items-center text-center max-w-xl mx-auto">
                    
                    <h2 class="text-xl font-bold text-gray-800 dark:text-gray-200 mb-6">
                        Lo sentimos, al no tener un profesional de la salud no puedes hacer uso de las funcionalidades de la aplicación
                    </h2>

                    <div class="bg-white dark:bg-gray-900 p-8 rounded-xl shadow-lg w-full max-w-sm border border-gray-200 dark:border-gray-700">
                        <h4 class="text-md font-semibold text-gray-800 dark:text-gray-100 mb-4">
                            Ingresa el código de enlace de tu nuevo profesional de la salud mental
                        </h4>
                        
                        <input 
                            type="text" 
                            v-model="linkCode" 
                            placeholder="Código de enlace" 
                            class="w-full p-3 border rounded-md mb-6 text-center dark:bg-gray-800 dark:border-gray-600 focus:ring-2 focus:ring-[#7DBFF8] dark:text-white"
                        />
                        
                        <button @click="attemptLink" class="w-full px-4 py-3 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded-lg font-semibold transition-colors">
                            Vincular
                        </button>

                        <button @click="openDeleteModal" class="mt-4 w-full px-4 py-2 text-red-500 hover:text-red-700 font-semibold rounded-lg transition-colors">
                            Eliminar cuenta
                        </button>
                    </div>
                </div>

                <router-view /> 
            </div>
        </main>
        <UserProfile />
    </div>
</template>

---

## **Script con Lógica de Eliminación (Modal)**

Vamos a agregar una simulación para el modal de eliminación de cuenta, ya que el usuario podría necesitar esa opción en esta pantalla.

```vue
<script setup lang="ts">
import { ref } from 'vue';
import Sidebar from "../components/SidebarPatient.vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import UserProfile from "../components/PatientProfile.vue"

const linkCode = ref('');
const showDeleteModal = ref(false); // Variable para el modal de eliminación

function attemptLink() {
    // 💡 AQUÍ va la llamada a tu API de Django para enviar el código de enlace.
    console.log(`Intentando vincular con código: ${linkCode.value}`);
    // Si la API tiene éxito, el backend debe actualizar el estado del usuario, 
    // y la aplicación cargará el contenido normal.
}

function openDeleteModal() {
    // Aquí podrías abrir el modal de confirmación de eliminación
    // Por ahora, solo cambiamos la variable, asumiendo que el modal se define en el layout padre
    console.log("Abriendo modal de eliminación...");
    showDeleteModal.value = true; 
    // Si estás usando un modal de otro componente, llama a la función o prop necesaria aquí.
}

// ... (Si necesitas la lógica de eliminación, la incluirías aquí)
</script>