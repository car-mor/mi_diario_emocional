<template>
  <div class="p-4 bg-gray-100 dark:bg-gray-900 min-h-full">

    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-500 dark:text-gray-400 mb-4">Cargando tus recuerdos...</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
        <div v-for="n in 4" :key="n" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <div class="h-5 bg-gray-300 dark:bg-gray-700 rounded w-3/4 mb-3"></div>
          <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-full mb-1"></div>
          <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-4/5 mb-4"></div>
          <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/3 ml-auto"></div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="text-center p-12 bg-red-100 dark:bg-red-900/20 rounded-lg">
      <h3 class="text-xl font-semibold text-red-600 dark:text-red-400">¡Oops! Ocurrió un error</h3>
      <p class="text-red-500 dark:text-red-300 mt-2">{{ error }}</p>
    </div>

    <div v-else>
      <div v-if="diaryEntries.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="entry in diaryEntries"
          :key="entry.id"
          @click="openModal(entry)"
          class="cursor-pointer bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300"
        >
          <div class="flex justify-between items-start">
            <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2 pr-4">{{ entry.title }}</h2>
            <div class="flex-shrink-0">
              <span v-for="emotion in entry.selected_emotions" :key="emotion" class="text-2xl">{{ emotionEmojis[emotion] || '❓' }}</span>
            </div>
          </div>
          <p class="text-gray-700 dark:text-gray-300 italic mb-4 line-clamp-2">
            "{{ entry.content }}"
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400 text-right">
            {{ formatDate(entry.entry_date) }}
          </p>
        </div>
      </div>

      <div v-else class="flex flex-col col-span-1 md:col-span-2 text-center py-10 items-center justify-center">
        <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4" />
        <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
          ¡Aún hay mucho por escribir!
        </h2>
        <p class="text-lg text-gray-600 dark:text-gray-400 mt-2">
          No tienes registros en tu diario. <router-link to="/diary-register" class="text-blue-500 hover:underline">¡Crea tu primera entrada!</router-link>
        </p>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4" @click="closeModal">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6 max-w-lg w-full relative" @click.stop>
        <button @click="closeModal" class="absolute top-3 right-3 text-gray-500 hover:text-gray-800 dark:hover:text-gray-200 transition-colors">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        <div v-if="selectedEntry" class="pr-8 pt-4">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            {{ selectedEntry.title }}
          </h2>
          <div class="mb-4">
            <span v-for="emotion in selectedEntry.selected_emotions" :key="emotion" class="text-3xl mr-1">{{ emotionEmojis[emotion] || '❓' }}</span>
          </div>
          <p class="text-gray-700 dark:text-gray-300 mb-6 whitespace-pre-line max-h-[60vh] overflow-y-auto">
            {{ selectedEntry.content }}
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400 text-right">
            {{ formatDate(selectedEntry.entry_date) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDiaryStore, type DiaryEntry } from '@/store/diary'; // 1. IMPORTA EL STORE Y EL TIPO
import { storeToRefs } from 'pinia';
import { IconBellRingingFilled } from "@tabler/icons-vue";

const emotionEmojis: Record<string, string> = {
  alegria:  '😊',
  tristeza: '😢',
  ira:      '😡',
  miedo:    '😨',
  asco:     '🤢',
  sorpresa: '😯',
};

// 2. CONECTA CON EL STORE
const diaryStore = useDiaryStore();
// Obtenemos 'entries' como una variable reactiva, que hemos renombrado a 'diaryEntries' para que coincida con tu template
const { entries: diaryEntries, loading, error } = storeToRefs(diaryStore);

// Ya no necesitas la lista de datos de prueba
// const diaryEntries = ref<DiaryEntry[]>([...]);

// --- Lógica del Modal (se mantiene igual) ---
const isModalOpen = ref(false);
const selectedEntry = ref<DiaryEntry | null>(null);

function openModal(entry: DiaryEntry) {
  selectedEntry.value = entry;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  // Es buena práctica esperar a que la animación de cierre termine un poco
  setTimeout(() => {
    selectedEntry.value = null;
  }, 300);
}

// 3. FUNCIÓN PARA FORMATEAR LA FECHA (para que se vea bien)
function formatDate(isoString: string) {
  const date = new Date(isoString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// 4. CARGA LOS DATOS CUANDO EL COMPONENTE SE MONTA
onMounted(() => {
  diaryStore.fetchEntries();
});
</script>
