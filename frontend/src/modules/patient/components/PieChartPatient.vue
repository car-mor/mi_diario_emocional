<template>
  <div class="p-6">
    <div class="w-full bg-white dark:bg-gray-800 rounded-lg shadow p-4 items-center justify-center min-h-[500px]">

      <div v-if="loading" class="flex flex-col items-center justify-center h-96">
        <p class="text-xl text-gray-500 dark:text-gray-400">Analizando emociones...</p>
      </div>
      <div v-else-if="error" class="flex flex-col items-center justify-center h-96">
        <p class="text-xl text-red-500">{{ error }}</p>
      </div>

      <div v-else-if="!chartInternalData || chartInternalData.length === 0" class="flex flex-col items-center justify-center h-96">
        <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4" />
        <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200 text-center">
          ¡Aún no hay suficientes datos!
        </h2>
        <p class="text-center text-xl text-gray-500 dark:text-gray-400 mt-2 px-4">
          No se encontraron combinaciones de emociones en este periodo.
        </p>
      </div>

      <div v-else>
        <div class="max-w-xl mx-auto" style="height: 500px;">
          <Pie :data="chartData" :options="chartOptions" />
        </div>
        <div class="flex justify-center mt-4 gap-4">
          <button @click="changeColorPalette" class="bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-2 px-4 rounded">
            Cambiar colores
          </button>
          <button @click="toggleDataDisplay" class="bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-2 px-4 rounded">
            {{ showPercentages ? 'Mostrar valores' : 'Mostrar porcentajes' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, type TooltipItem } from 'chart.js';
import { IconBellRingingFilled } from "@tabler/icons-vue";
import * as DiaryService from '@/modules/diary/services/diaryServices';
ChartJS.register(Title, Tooltip, Legend, ArcElement);

// 1. ACEPTA LOS DATOS COMO UNA PROP
// Estos son los datos que el componente padre (PatientDetails.vue) le pasa.
const props = defineProps<{
  combinationData?: [string, number][];
}>();

const chartInternalData = ref<[string, number][]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  loading.value = true;
  error.value = null;

  if (props.combinationData) {
    // Si el padre nos dio los datos, los usamos.
    chartInternalData.value = props.combinationData;
    loading.value = false;
  } else {
    // Si no, este componente busca sus propios datos (caso del paciente).
    try {
      const response = await DiaryService.getEmotionCombinations();
      chartInternalData.value = response.data;
    } catch (err) {
      console.error('Fallo al obtener datos para la gráfica:', err);
      error.value = "No se pudieron cargar los datos del análisis.";
    } finally {
      loading.value = false;
    }
  }
});

// 2. ESTADOS INTERNOS DEL COMPONENTE (siguen usando ref)
// Estas variables solo afectan a cómo se ve la gráfica, no a los datos en sí.
const activePaletteIndex = ref(0);
const showPercentages = ref(false);

// Paletas de colores (constante)
const colorPalettes = [
  ['#7DBFF8', '#B5D8B8', '#EDA1A1', '#FFD1DC', '#FFA07A'],
  ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
  ['#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E', '#00B894']
];

// Funciones para manipular el estado interno
const changeColorPalette = () => {
  activePaletteIndex.value = (activePaletteIndex.value + 1) % colorPalettes.length;
};

const toggleDataDisplay = () => {
  showPercentages.value = !showPercentages.value;
};

// 3. LA LÓGICA COMPUTADA AHORA USA `props.combinationData`
const chartData = computed(() => {
  const currentPalette = colorPalettes[activePaletteIndex.value];
  return {
    labels: chartInternalData.value.map(item => item[0]),       // <-- Usa el estado interno
    datasets: [{
      data: chartInternalData.value.map(item => item[1]),       // <-- Usa el estado interno
      backgroundColor: chartInternalData.value.map((_, index) => currentPalette[index % currentPalette.length]),
      borderColor: '#ffffff',
      borderWidth: 2,
    }]
  };
});

// Opciones de la gráfica (depende del estado interno `showPercentages`)
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { padding: 20, usePointStyle: true, font: { size: 12 } }
    },
    tooltip: {
      callbacks: {
        label: function(context: TooltipItem<'pie'>) {
          const label = context.label || '';
          const value = context.parsed;
          if (context.dataset.data.length === 0) return label;

          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
          if (total === 0) return `${label}: ${value}`;

          const percentage = ((value / total) * 100).toFixed(1);

          return showPercentages.value ? `${label}: ${percentage}%` : `${label}: ${value}`;
        }
      }
    }
  }
}));
</script>
