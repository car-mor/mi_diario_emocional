<template>
  <div class="flex h-screen dark:bg-gray-900">

    <main class="flex-1 flex flex-col overflow-hidden">
        <StreakAndTitle
          title="Diario: Historial de entradas"
          :streak-count="streakCount"
        />
      <div class="flex-1 p-4 sm:p-6 overflow-y-auto">

        <div class="p-4">
          <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-200">
            Un vistazo al pasado...
          </h2>
        </div>

        <div class="text-center lg:text-left px-4 pb-4">
          <p class="text-lg text-gray-600 dark:text-gray-300">
            ¡Hola! Te presentamos la sección de recuerdos, en donde puedes consultar tus escritos anteriores. Aquí podrás ver todas las entradas que has realizado en tu diario, ¡Revive tus pensamientos y emociones pasadas!
          </p>
        </div>
  <div class="px-4">
    <div v-if="loading">
      <p class="text-center text-gray-500 dark:text-gray-400">Cargando tu historial...</p>
      <div v-for="n in 3" :key="n" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-4 animate-pulse">
        <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
        <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
        <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-full mb-1"></div>
        <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-full"></div>
      </div>
    </div>

    <div v-else-if="error" class="text-center p-8 bg-red-100 dark:bg-red-900/20 rounded-lg">
      <p class="text-red-600 dark:text-red-400 font-semibold">¡Oops! Ocurrió un error</p>
      <p class="text-red-500 dark:text-red-300 mt-2">{{ error }}</p>
    </div>

    <div v-else-if="entries.length === 0" class="text-center p-12 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
      <p class="text-xl text-gray-600 dark:text-gray-300">Aún no has escrito ninguna entrada en tu diario.</p>
      <router-link to="/diary-register" class="mt-4 inline-block px-6 py-2 bg-[#7DBFF8] text-white font-semibold rounded-lg">
        Escribir mi primera entrada
      </router-link>
    </div>

    <div v-else>
      <div v-for="entry in entries" :key="entry.id" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-4 transition-transform hover:scale-[1.02]">
        <div class="flex justify-between items-start">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ entry.title }}</h3>
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(entry.entry_date) }} hrs</span>
        </div>
        <p class="mt-4 text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words">
          {{ entry.content }}
        </p>
        <div class="mt-2">
          <label class="text-sm font-medium text-gray-600 dark:text-gray-300 mr-2">Este día me sentí:</label>
          <span v-for="emotion in entry.selected_emotions" :key="emotion" class="text-2xl mr-1">{{ emotionEmojis[emotion] || '❓' }}</span>
        </div>
      </div>
    </div>
  </div>
      </div>
    </main>
    <UserProfile />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useDiaryStore } from '@/store/diary';
import { storeToRefs } from 'pinia';
import UserProfile from "@/modules/patient/components/PatientProfile.vue";
   import StreakAndTitle from "../components/StreakAndTitlePatient.vue";
import { computed } from 'vue';
  import { useAuthStore } from '@/store/auth';
    const authStore = useAuthStore();

interface PatientProfile {
    name: string;
    paternal_last_name: string;
    maternal_last_name: string;
    email: string;
    alias: string;
    gender: string;
    professional_name?: string; // Es opcional y puede ser nulo
    is_linked: boolean;
    current_streak: number;
}
const streakCount = computed(() => {
  // Primero, verificamos si el usuario es un paciente y si su perfil ha cargado
  if (authStore.userType === 'patient' && authStore.userProfile) {
    // Si es así, le decimos a TypeScript que trate el perfil como un PatientProfile
    // y accedemos a 'current_streak' de forma segura.
    return (authStore.userProfile as PatientProfile).current_streak || 0;
  }
  // Si no es un paciente, la racha es 0.
  return 0;
});
// 1. Conectar con el Store de Pinia
const diaryStore = useDiaryStore();

// 2. Obtener el estado del store de forma reactiva
const { entries, loading, error } = storeToRefs(diaryStore);

// Mapeo de valores de emoción a emojis (para mostrar en la UI)
const emotionEmojis: Record<string, string> = {
  alegria: '😊',
  tristeza: '😢',
  ira: '😡',
  miedo: '😨',
  asco: '🤢',
  sorpresa: '😯',
};

// 3. Función para formatear la fecha
function formatDate(isoString: string) {
  const date = new Date(isoString);
  return date.toLocaleString('es-ES', { // Cambiado a toLocaleString
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

// 4. Cargar las entradas cuando el componente se monta
onMounted(() => {
  diaryStore.fetchEntries();
});
</script>
