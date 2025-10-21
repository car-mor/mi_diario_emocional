<template>
  <div class="w-full h-96 bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex flex-col items-center justify-center">

    <div v-if="loading" class="flex flex-col items-center justify-center h-full">
        <p class="text-xl text-gray-500 dark:text-gray-400">Analizando palabras...</p>
    </div>
    <div v-else-if="error" class="flex flex-col items-center justify-center h-full">
        <p class="text-xl text-red-500">{{ error }}</p>
    </div>

    <div v-else-if="!wordsInternalData || wordsInternalData.length === 0" class="flex flex-col items-center justify-center text-center">
      <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4" />
      <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
        ¡Aún hay mucho por escribir!
      </h2>
      <p class="text-xl text-gray-500 dark:text-gray-400 mt-2 px-4">
        No hay suficientes palabras en este periodo para generar la nube.
      </p>
    </div>

    <div v-else class="w-full h-full flex flex-col">
      <div class="flex-grow">
        <vue-word-cloud
          :words="wordsInternalData"
          font-family="Quicksand, Arial, sans-serif"
          :color="randomColor"
          :animation-duration="2000"
        />
      </div>
      <div class="flex-shrink-0 flex justify-center mt-4">
        <button
          @click="changeColorPalette"
          class="bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-2 px-4 rounded"
        >
          Cambiar colores
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import VueWordCloud from "vuewordcloud";
import { IconBellRingingFilled } from "@tabler/icons-vue";
import * as DiaryService from '@/modules/diary/services/diaryServices';
// --- ACEPTA LOS DATOS COMO UNA PROP ---
// El componente padre (PatientDetails.vue) le pasará la lista de palabras.
const props = defineProps<{
  words?: [string, number][];
}>();

const wordsInternalData = ref<[string, number][]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  loading.value = true;
  error.value = null;

  if (props.words) {
    // Si nos pasan la prop, la usamos.
    wordsInternalData.value = props.words;
    loading.value = false;
  } else {
    // Si no, buscamos nuestros propios datos.
    try {
      const response = await DiaryService.getWordFrequency();
      wordsInternalData.value = response.data;
    } catch (err) {
      console.error('Fallo al obtener datos para la nube:', err);
      error.value = "No se pudieron cargar los datos del análisis.";
    } finally {
      loading.value = false;
    }
  }
});
// --- ESTADOS Y LÓGICA INTERNA DEL COMPONENTE ---
// Estas variables solo afectan a la apariencia de la nube, no a los datos.
const palettes = [
  ['#0E7891', '#096097', '#7DBFF8'], // Paleta Azul
  ['#EDA1A1', '#FFD1DC', '#FF69B4'], // Paleta Rosa
  ['#B5D8B8', '#90EE90', '#32CD32']  // Paleta Verde
];

const activePaletteIndex = ref(0);

// Función para cambiar de paleta
const changeColorPalette = () => {
  activePaletteIndex.value = (activePaletteIndex.value + 1) % palettes.length;
};

// Función que elige un color al azar de la paleta activa para cada palabra
const randomColor = () => {
  const currentPalette = palettes[activePaletteIndex.value];
  return currentPalette[Math.floor(Math.random() * currentPalette.length)];
};
</script>
