<template>
  <div class="p-6">
    <div class="w-full bg-white dark:bg-gray-800 rounded-lg shadow p-4 items-center justify-center">
      
      <!-- Mensaje cuando no hay datos -->
      <div v-if="combinationData.length === 0" class="flex flex-col items-center justify-center h-96">
        <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4" />
        <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200 text-center">
          ¡Aún no hay suficientes datos!
        </h2>
        <p class="text-center text-xl text-gray-500 dark:text-gray-400 mt-2 px-4">
          Necesitas más entradas en tu diario para generar el análisis de emociones combinadas.
        </p>
      </div>

      <!-- Gráfica de pastel -->
      <div v-if="combinationData.length > 0" class="max-w-xl mx-auto" style="height: 500px;">
        <Pie :data="chartData" :options="chartOptions" />
      </div>
      
      <!-- Botones de control -->
      <div v-if="combinationData.length > 0" class="flex justify-center mt-4 gap-4">
        <button
          @click="changeColorPalette"
          class="bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-2 px-4 rounded"
        >
          Cambiar colores
        </button>
        <button
          @click="toggleDataDisplay"
          class="bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-2 px-4 rounded"
        >
          {{ showPercentages ? 'Mostrar valores' : 'Mostrar porcentajes' }}
        </button>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { IconBellRingingFilled } from "@tabler/icons-vue";

//backend
/*
import axios from 'axios';
import { onMounted } from 'vue';
*/
ChartJS.register(Title, Tooltip, Legend, ArcElement);

// Datos de ejemplo: Array de combinaciones con sus frecuencias
const combinationData: [string, number][] = [
  ["Ansiedad-Felicidad", 50],
  ["Felicidad-Tristeza", 90],
  ["Tristeza-Estrés", 85],
  ["Estrés-Calma", 75],
  ["Calma-Motivación", 60],
];

// Simula un array vacío para probar el mensaje
//const combinationData: [string, number][] = [];

//backend
/*
const loading = ref(true);
const error = ref(false);

onMounted(async () => {
  try {
    const response = await axios.get('/api/frecuencia-combinaciones');
    combinationData.values = response.data.combinationFrequency;
    loading.value = false;
  } catch (err) {
    console.error('Failed to fetch pie chart data:', err);
    error.value = true;
    loading.value = false;
  }
});*/

// Paletas de colores
const colorPalettes = [
  ['#7DBFF8', '#B5D8B8', '#EDA1A1', '#FFD1DC', '#FFA07A', '#98D8C8'], // Paleta suave
  ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'], // Paleta vibrante
  ['#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E', '#6C5CE7', '#00B894']  // Paleta moderna
];

const activePaletteIndex = ref(0);
const showPercentages = ref(false);

// Función para cambiar de paleta
const changeColorPalette = () => {
  activePaletteIndex.value = (activePaletteIndex.value + 1) % colorPalettes.length;
};

// Función para alternar entre valores y porcentajes
const toggleDataDisplay = () => {
  showPercentages.value = !showPercentages.value;
};

// Datos computados para la gráfica
const chartData = computed(() => {
  const currentPalette = colorPalettes[activePaletteIndex.value];
  
  return {
    labels: combinationData.map(item => item[0]),
    datasets: [
      {
        backgroundColor: combinationData.map((_, index) => 
          currentPalette[index % currentPalette.length]
        ),
        borderColor: '#ffffff',
        borderWidth: 2,
        data: combinationData.map(item => item[1]),
      }
    ]
  };
});

// Opciones de la gráfica
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 20,
        usePointStyle: true,
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          const label = context.label || '';
          const value = context.parsed;
          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(1);
          
          if (showPercentages.value) {
            return `${label}: ${percentage}%`;
          } else {
            return `${label}: ${value}`;
          }
        }
      }
    }
  }
}));
</script>