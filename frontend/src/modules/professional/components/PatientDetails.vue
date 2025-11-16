<template>
  <div class="p-4 sm:p-6 dark:bg-gray-900 min-h-screen overflow-x-hidden">
    <div class="max-w-7xl mx-auto">

      <div v-if="loading" class="text-center py-20">
        <p class="text-xl text-gray-500 dark:text-gray-400">Cargando detalles del paciente...</p>
      </div>
      <div v-else-if="error" class="text-center py-20 bg-red-50 dark:bg-red-900/20 p-8 rounded-lg">
        <h2 class="text-2xl font-bold text-red-600 dark:text-red-400">Error al Cargar</h2>
        <p class="text-red-500 dark:text-red-300 mt-2">{{ error }}</p>
        <button @click="goBack" class="mt-6 px-4 py-2 bg-red-500 text-white font-semibold rounded-lg">
          Volver
        </button>
      </div>

      <div v-else-if="patient">

        <div class="flex items-center justify-between mb-8">
          <button @click="goBack" class="p-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-800 dark:text-white" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15 6l-6 6l6 6"></path></svg>
          </button>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white flex-grow text-center lg:text-left ml-4">
            Paciente: {{ patient.name }}
          </h1>
        </div>

        <div class="my-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border dark:border-gray-700">
          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">

            <div class="md:col-span-2">
              <label for="week-selector" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Análisis por Semana</label>
              <select id="week-selector" v-model="selectedWeek" @change="handleWeekChange" class="text-gray-700 dark:text-gray-300 mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm dark:bg-gray-700 focus:border-blue-500 focus:ring-blue-500">
                <option v-for="week in availableWeeks" :key="week.week_number" :value="week.start_date">
                  {{ week.display_text }}
                </option>
              </select>
            </div>

            <p class="text-center text-gray-500 dark:text-gray-400 font-bold md:col-span-1">Ó</p>

            <div class="md:col-span-2 grid grid-cols-2 gap-4">
              <div>
                <label for="start-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Desde</label>
                <input type="date" id="start-date" v-model="customStartDate" class="text-gray-700 dark:text-gray-300 mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm dark:bg-gray-700 focus:border-blue-500 focus:ring-blue-500">
              </div>
              <div>
                <label for="end-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Hasta</label>
                <input type="date" id="end-date" v-model="customEndDate" class="text-gray-700 dark:text-gray-300 mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm dark:bg-gray-700 focus:border-blue-500 focus:ring-blue-500">
              </div>
            </div>
          </div>
          <div class="flex justify-center md:justify-end mt-4">
            <button @click="applyCustomFilter" class="bg-[#70BFE9] hover:bg-[#5DA6C8] text-white font-semibold py-2 px-4 rounded-md w-full md:w-auto">
              Filtrar por Fecha
            </button>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl mb-8 overflow-x-auto">
          <table class="min-w-full">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nombre</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Edad</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Género</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Correo</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Alias</th>
                <th class="px-6 py-3 text-center text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Avatar</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-semibold whitespace-nowrap">{{ patient.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">{{ patient.age }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">{{ genderMap[patient.gender] || patient.gender }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">{{ patient.email }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">{{ patient.alias }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 text-center">
                  <img
                                        :src="patient.avatar_url || '/images/avatar-icon.png'"
                                        :alt="`Avatar de ${patient.alias}`"
                                        class="w-15 h-15 rounded-full object-cover border-2 border-blue-400"
                                    />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-800 dark:text-white mt-8 mb-4">Análisis de Entradas</h2>
        <div class="border-b border-gray-300 dark:border-gray-700 mb-6">
          <div class="overflow-x-auto">
            <div class="flex space-x-2 sm:space-x-4">
              <button @click="activeTab = 'historial'" :class="tabClass('historial')" class="whitespace-nowrap">Historial</button>
              <button @click="activeTab = 'grafica'" :class="tabClass('grafica')" class="whitespace-nowrap">Emociones Combinadas</button>
              <button @click="activeTab = 'nube'" :class="tabClass('nube')" class="whitespace-nowrap">Nube de Palabras</button>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-4 sm:p-6 min-h-[500px]">

          <div v-if="activeTab === 'historial'">
            <div v-if="!hasData" class="flex justify-center items-center h-[400px] text-center">
              <p class="text-xl text-gray-600 dark:text-gray-300">Este paciente aún no tiene entradas en su diario.</p>
            </div>
            <div v-else class="space-y-6">
              <div
                v-for="entry in diaryHistory"
                :key="entry.id"
                class="border dark:border-gray-700 rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-lg dark:hover:bg-gray-700 whitespace-pre-wrap break-words"
                @click="toggleExpand(entry.id)"
              >
                <h3 class="font-bold text-lg dark:text-white">{{ entry.title }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">{{ new Date(entry.entry_date).toLocaleString() }}</p>

                <p v-if="expandedEntryId === entry.id" class="text-gray-700 dark:text-gray-300 text-sm mb-4 whitespace-pre-wrap">
                  {{ entry.content }}
                </p>
                <p v-else class="text-gray-700 dark:text-gray-300 text-sm mb-4 italic">
                  "{{ entry.content.substring(0, 200) }}..." (clic para expandir)
                </p>

                <div class="flex flex-col md:flex-row gap-4 pt-3 border-t dark:border-gray-600">
                  <div class="flex-1">
                    <h4 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Sentimiento seleccionado:</h4>
                    <div v-if="entry.selected_emotions && entry.selected_emotions.length > 0" class="flex flex-wrap gap-2">
                      <span v-for="emotion in entry.selected_emotions" :key="emotion" class="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 px-2.5 py-1 rounded-full font-medium">
                        {{ emotion }}
                      </span>
                    </div>
                    <p v-else class="text-sm text-gray-400 dark:text-gray-500 italic">Ninguno reportado.</p>
                  </div>

                  <div class="flex-1">
<h4 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Análisis de IA:</h4>

  <div
    v-if="entry.analyzed_emotions && entry.analyzed_emotions.length > 0 && entry.analyzed_emotions[0] !== 'neutro'"
    class="space-y-2"
  >
    <!-- Badges con emociones detectadas -->
    <div class="flex flex-wrap gap-2">
      <span
        v-for="emotion in entry.analyzed_emotions"
        :key="emotion"
        :class="getEmotionBadgeClass(emotion)"
        class="text-xs px-3 py-1.5 rounded-full font-medium inline-flex items-center gap-1.5"
      >
        <span class="capitalize">{{ emotion }}</span>
        <span class="font-bold">
          {{ getEmotionPercentage(entry, emotion) }}%
        </span>
      </span>
    </div>

    <!-- Dropdown expandible para todas las probabilidades -->
    <details
      v-if="entry.analyzed_scores && Object.keys(entry.analyzed_scores).length > 0"
      class="group"
    >
      <summary class="text-xs text-blue-500 dark:text-blue-400 cursor-pointer hover:underline select-none list-none flex items-center gap-1">
        <svg
          class="w-4 h-4 transition-transform group-open:rotate-90"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <span>Ver todas las probabilidades</span>
      </summary>

      <!-- Contenido del dropdown -->
      <div class="mt-2 ml-5 space-y-1.5 text-xs bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 border border-gray-200 dark:border-gray-600">
        <div
          v-for="[emotion, prob] in getSortedEmotionScores(entry)"
          :key="emotion"
          class="flex justify-between items-center py-1 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors"
        >
          <span class="capitalize text-gray-700 dark:text-gray-300 font-medium">
            {{ emotion }}
          </span>

          <!-- Mini barra de progreso -->
          <div class="flex items-center gap-2 flex-1 max-w-[150px] ml-4">
            <div class="flex-1 bg-gray-200 dark:bg-gray-600 rounded-full h-1.5 overflow-hidden">
              <div
                :class="getEmotionColorClass(emotion)"
                class="h-full rounded-full transition-all duration-300"
                :style="{ width: `${Math.round(prob * 100)}%` }"
              ></div>
            </div>
            <span class="font-bold text-gray-800 dark:text-gray-200 w-10 text-right">
              {{ Math.round(prob * 100) }}%
            </span>
          </div>
        </div>
      </div>
    </details>
  </div>

  <p
    v-else
    class="text-sm text-gray-400 dark:text-gray-500 italic"
  >
    Análisis neutral.
  </p>
</div>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'grafica'">
            <PieChartPatient
              :combination-data="emotionCombinations"
              :loading="loading"
              :error="error"
            />
          </div>
          <div v-else-if="activeTab === 'nube'">
            <WordCloudPatient
              :words="wordFrequency"
              :loading="loading"
              :error="error"
            />
          </div>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-between bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mt-8 gap-4">
          <div class="flex items-center space-x-3 text-center sm:text-left">
            <p class="text-sm text-gray-600 dark:text-gray-300">
              <span v-if="reportInfo?.is_available">
                Descargar reporte del periodo de tiempo seleccionado.
              </span>
              <span v-else>
                <span v-if="diaryHistory.length === 0">
                  El primer reporte estará disponible 7 días después de que el paciente escriba por primera vez.
                </span>
                <span v-else>
                  El próximo reporte para este periodo estará disponible el:
                  <span class="font-semibold">{{ reportInfo?.next_report_date }}</span>
                </span>
              </span>
            </p>
          </div>
          <button
            @click="downloadPdf"
            class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors w-full sm:w-auto flex-shrink-0"
            :disabled="isDownloading || !reportInfo?.is_available"
            :class="{ 'opacity-50 cursor-not-allowed': isDownloading || !reportInfo?.is_available }">
            {{ isDownloading ? 'Generando...' : 'Descargar PDF' }}
          </button>
        </div>

      </div>
    </div>
  </div>

  <div v-if="showReportUnavailableModal" class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-2xl max-w-sm w-full text-center mx-4">
      <div class="w-16 h-16 mx-auto bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-[#7DBFF8] dark:text-blue-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 21a9 9 0 0 1 -9 -9a9 9 0 0 1 9 -9a9 9 0 0 1 9 9a9 9 0 0 1 -9 9z"></path><path d="M12 8l0 4"></path><path d="M12 16l.01 0"></path></svg>
      </div>
      <h3 class="text-xl font-bold mb-4 dark:text-white">Reporte Aún No Disponible</h3>
      <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
        El reporte semanal de este paciente estará disponible a partir del:
        <span class="font-semibold text-[#7DBFF8] dark:text-blue-400 block mt-2">{{ reportInfo?.next_report_date }}</span>
      </p>
      <button
        @click="showReportUnavailableModal = false"
        class="px-6 py-2 bg-[#7DBFF8] hover:bg-[#2563eb] text-white font-semibold rounded-lg w-full transition-colors"
      >
        Entendido
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PieChartPatient from '@/modules/patient/components/PieChartPatient.vue';
import WordCloudPatient from '@/modules/patient/components/WordCloudPatient.vue';
import * as ProfessionalService from '@/modules/professional/services/professionalServices';
// --- CORRECCIÓN EN IMPORTS ---
// Eliminamos ReportWeek y ReportInfo de aquí, ya que no se usan directamente como tipos
import type { Patient, DiaryEntry } from '@/modules/professional/services/professionalServices';
const route = useRoute();
const router = useRouter();

// --- ESTADOS DE PÁGINA ---
const loading = ref(true);
const error = ref<string | null>(null);
const activeTab = ref<'historial' | 'grafica' | 'nube'>('historial');
const isDownloading = ref(false);
const showReportUnavailableModal = ref(false);

// Variables para los datos de la API
const patient = ref<Patient | null>(null);
const diaryHistory = ref<DiaryEntry[]>([]);
const emotionCombinations = ref<[string, number][]>([]);
const wordFrequency = ref<[string, number][]>([]);
const reportInfo = ref<ProfessionalService.ReportInfo | null>(null);
// --- ESTADOS PARA EL FILTRO ---
const availableWeeks = ref<ProfessionalService.ReportWeek[]>([]);
const selectedWeek = ref<string | null>(null); // Guardará el start_date de la semana
const customStartDate = ref('');
const customEndDate = ref('');
const activeFilter = ref<{ type: 'week' | 'custom', dates: { startDate: string, endDate: string } | null }>({ type: 'week', dates: null });
const expandedEntryId = ref<string | null>(null);
const patientId = route.params.id as string;

// --- LÓGICA COMPUTADA ---
const hasData = computed(() => diaryHistory.value.length > 0);
function getEmotionPercentage(entry: DiaryEntry, emotion: string): number {
  if (!entry.analyzed_scores || !entry.analyzed_scores[emotion]) {
    return 0;
  }

  const probability = entry.analyzed_scores[emotion];
  return Math.round(probability * 100);
}
/**
 * Obtiene las clases de color para el badge según la emoción
 */
function getEmotionBadgeClass(emotion: string): string {
  const emotionClasses: Record<string, string> = {
    alegria: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    tristeza: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    ira: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    miedo: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    sorpresa: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300',
    asco: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
  };

  return emotionClasses[emotion] || 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
}

function getEmotionColorClass(emotion: string): string {
  const emotionColors: Record<string, string> = {
    alegria: 'bg-yellow-400 dark:bg-yellow-500',
    tristeza: 'bg-blue-500 dark:bg-blue-400',
    ira: 'bg-red-500 dark:bg-red-400',
    miedo: 'bg-purple-500 dark:bg-purple-400',
    sorpresa: 'bg-pink-500 dark:bg-pink-400',
    asco: 'bg-green-500 dark:bg-green-400'
  };
  return emotionColors[emotion] || 'bg-blue-500 dark:bg-blue-400';
}

function getSortedEmotionScores(entry: DiaryEntry): Array<[string, number]> {
  if (!entry.analyzed_scores) {
    return [];
  }

  return Object.entries(entry.analyzed_scores)
    .sort((a, b) => b[1] - a[1]); // Ordenar de mayor a menor
}
const tabClass = (tabName: 'historial' | 'grafica' | 'nube') => ({
  'py-2 px-4 text-lg font-medium transition-colors border-b-2': true,
  'text-blue-500 border-blue-500 dark:text-blue-400 dark:border-blue-400': activeTab.value === tabName,
  'text-gray-500 border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300': activeTab.value !== tabName,
});

// --- MÉTODOS DE ACCIÓN ---
function goBack() {
  router.back();
}

function toggleExpand(entryId: string) {
  // Si el ID clicado ya es el que está expandido, lo cerramos (null)
  if (expandedEntryId.value === entryId) {
    expandedEntryId.value = null;
  } else {
    // Si no, expandimos este
    expandedEntryId.value = entryId;
  }
}

const genderMap: Record<string, string> = {
  male: 'Masculino',
  female: 'Femenino',
  non_binary: 'No binario',
  other: 'Otro'
};

const fetchPatientData = async () => {
  if (!patientId) return;

  loading.value = true;
  error.value = null;

  try {
    const response = await ProfessionalService.getPatientDetails(patientId, activeFilter.value.dates || undefined);
    const data = response.data;

    patient.value = data.patient_details;
    diaryHistory.value = data.diary_history;
    emotionCombinations.value = data.emotion_combinations;
    wordFrequency.value = data.word_frequency;
    reportInfo.value = data.report_info;
  } catch (err) {
    console.error("Error al cargar los detalles del paciente:", err);
    error.value = "No se pudieron cargar los datos del paciente para el periodo seleccionado.";
  } finally {
    loading.value = false;
  }
};

const applyCustomFilter = () => {
  if (customStartDate.value && customEndDate.value) {
    activeFilter.value = {
      type: 'custom',
      dates: { startDate: customStartDate.value, endDate: customEndDate.value }
    };
    selectedWeek.value = null; // Deseleccionamos la semana para evitar inconsistencias
    fetchPatientData(); // Recargamos los datos con el nuevo filtro
  } else {
    alert("Por favor, selecciona una fecha de inicio y de fin.");
  }
};

const handleWeekChange = () => {
  if (selectedWeek.value) {
    const weekInfo = availableWeeks.value.find(w => w.start_date === selectedWeek.value);
    if (weekInfo) {
      activeFilter.value = {
        type: 'week',
        dates: { startDate: weekInfo.start_date, endDate: weekInfo.end_date }
      };
      customStartDate.value = ''; // Limpiamos el filtro custom
      customEndDate.value = '';
      fetchPatientData(); // Recargamos los datos para la semana seleccionada
    }
  }
};

onMounted(async () => {
  if (!patientId) {
    error.value = "No se especificó un ID de paciente.";
    loading.value = false;
    return;
  }

  try {
    // 1. Cargamos la lista de semanas disponibles para el selector
    const weeksResponse = await ProfessionalService.getReportWeeks(patientId);
    availableWeeks.value = weeksResponse.data;

    // 2. Si hay semanas, seleccionamos la más reciente y cargamos sus datos
    if (weeksResponse.data.length > 0) {
      selectedWeek.value = weeksResponse.data[0].start_date;
      handleWeekChange(); // Usamos el handler para establecer el filtro y cargar los datos
    } else {
      // Si no hay semanas (paciente sin entradas), igual cargamos la info del paciente
      await fetchPatientData();
      loading.value = false;
    }
  } catch (err) {
    console.error("Error al inicializar la vista:", err);
    error.value = "No se pudieron cargar los datos iniciales del paciente.";
    loading.value = false;
  }
});

async function downloadPdf() {
  if (!reportInfo.value?.is_available) {
    showReportUnavailableModal.value = true;
    return;
  }

  isDownloading.value = true;
  try {
    const response = await ProfessionalService.downloadPatientReport(
      patientId,
      activeFilter.value.dates || undefined
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const contentDisposition = response.headers['content-disposition'];
    let fileName = `reporte_semanal.pdf`;
    if (contentDisposition) {
        const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
        if (fileNameMatch && fileNameMatch.length === 2) fileName = fileNameMatch[1];
    }

    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

  } catch (err) {
    console.error("Error al descargar el PDF:", err);
  } finally {
    isDownloading.value = false;
  }
}
</script>
