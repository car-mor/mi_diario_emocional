<template>
    <div class="w-full h-96 bg-white dark:bg-gray-800 rounded-lg shadow p-4 items-center justify-center">

    <div v-if="words.length === 0" class="flex flex-col items-center justify-center">
        <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4" />
        <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
            ¡Aún hay mucho por escribir!
        </h2>
        <p class="text-center text-xl text-gray-500 dark:text-gray-400 mt-2 px-4">
            Aún no hay suficientes palabras para generar la nube. Escribe más en tu diario y vuelve a intentarlo.
        </p>
    </div>
        <!-- Componente de Nube de Palabras -->
        <vue-word-cloud
            :words="words"
            font-family="Quicksand, Arial, sans-serif"
            :color="randomColor"
            :animation-duration="2000"
            :animation-steps="15"
            shape="star"
        />
    </div>
    <div v-if="words.length > 0" class="flex justify-center mt-4 gap-4">
        <button
            @click="changeColorPalette"
            class="bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-bold py-2 px-4 rounded"
        >
            Cambiar colores
        </button>
    </div>
</template>

<script setup lang="ts">
import { IconBellRingingFilled } from "@tabler/icons-vue"
import { ref } from 'vue';
import VueWordCloud from "vuewordcloud";
//backend
/*
import axios from 'axios';
import { onMounted } from 'vue';*/

// Datos de ejemplo: Array de palabras con sus frecuencias
const words: [string, number][] = [
  ["feliz", 50],
  ["triste", 30],
  ["emocionado", 20],
  ["ansioso", 15],
  ["calmado", 10],
  ["motivado", 25],
  ["estresado", 18],
  ["sorprendido", 22],
  ["frustrado", 12],
  ["agradecido", 100],
  ["confundido", 8],
  ["relajado", 14],
  ["enojado", 5],
  ["esperanzado", 28],
  ["aburrido", 7],
];

// Simula un array vacío para probar el mensaje
 //const words: [string, number][] = [];

//backend
/*
const loading = ref(true);
const error = ref(false);*/

const palettes = [
  ['#0E7891', '#096097', '#7DBFF8'], // Paleta Azul
  ['#EDA1A1', '#FFD1DC', '#FF69B4'], // Paleta Rosa
  ['#B5D8B8', '#90EE90', '#32CD32']  // Paleta Verde
];

//backend
/*
onMounted(async () => {
  try {
    const response = await axios.get('/api/frecuencia-palabras');
    words.values = response.data.wordFrequency;
    loading.value = false;
  } catch (err) {
    console.error('Failed to fetch word cloud data:', err);
    error.value = true;
    loading.value = false;
  }
});*/

// Variable reactiva para la paleta de colores activa
const activePaletteIndex = ref(0);

// Función para cambiar de paleta
const changeColorPalette = () => {
  activePaletteIndex.value = (activePaletteIndex.value + 1) % palettes.length;
};

// Función para elegir un color de la paleta activa
const randomColor = () => {
  const currentPalette = palettes[activePaletteIndex.value];
  return currentPalette[Math.floor(Math.random() * currentPalette.length)];
};
</script>