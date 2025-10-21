<template>
  <div class="p-6 dark:bg-gray-900 min-h-screen">
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
          <button @click="goBack" class="p-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-800 dark:text-white" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15 6l-6 6l6 6"></path></svg>
          </button>
          <h1 class="text-3xl font-bold text-gray-800 dark:text-white flex-grow text-center lg:text-left ml-4">
            Paciente: {{ patient.name }}
          </h1>
        </div>
        <div class="my-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border dark:border-gray-700">
  <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">

    <div class="md:col-span-2">
      <label for="week-selector" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Análisis por Semana</label>
      <select id="week-selector" v-model="selectedWeek" @change="handleWeekChange" class="mt-1 block w-full rounded-md ...">
        <option v-for="week in availableWeeks" :key="week.week_number" :value="week.start_date">
          {{ week.display_text }}
        </option>
      </select>
    </div>

    <p class="text-center text-gray-500 dark:text-gray-400 font-bold md:col-span-1">Ó</p>

    <div class="md:col-span-2 grid grid-cols-2 gap-4">
      <div>
        <label for="start-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Desde</label>
        <input type="date" id="start-date" v-model="customStartDate" class="mt-1 block w-full rounded-md ...">
      </div>
      <div>
        <label for="end-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Hasta</label>
        <input type="date" id="end-date" v-model="customEndDate" class="mt-1 block w-full rounded-md ...">
      </div>
    </div>
  </div>
  <div class="flex justify-end mb-8">
      <button @click="applyCustomFilter" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md">
        Filtrar por Fecha
      </button>
  </div>
</div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 mb-8">
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
              <tr class="block lg:table-row p-4 lg:p-0">
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell font-semibold" data-label="Nombre">{{ patient.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Edad">{{ patient.age }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Género">{{ patient.gender }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Correo">{{ patient.email }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Alias">{{ patient.alias }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Avatar">
                  <img :src="patient.avatar_url" :alt="`Avatar de ${patient.alias}`" class="w-10 h-10 rounded-full object-cover border-2 border-blue-400" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-800 dark:text-white mt-8 mb-4">Análisis de Entradas</h2>
        <div class="flex border-b border-gray-300 dark:border-gray-700 mb-6">
          <button @click="activeTab = 'historial'" :class="tabClass('historial')">Historial</button>
          <button @click="activeTab = 'grafica'" :class="tabClass('grafica')">Emociones Combinadas</button>
          <button @click="activeTab = 'nube'" :class="tabClass('nube')">Nube de Palabras</button>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 min-h-[500px]">
          <div v-if="activeTab === 'historial'">
            <div v-if="!hasData" class="flex justify-center items-center h-[400px]">
              <p class="text-xl text-gray-600 dark:text-gray-300">Este paciente aún no tiene entradas en su diario.</p>
            </div>
            <div v-else class="space-y-6">
              <div v-for="entry in diaryHistory" :key="entry.id" class="border dark:border-gray-700 rounded-lg p-4">
                <h3 class="font-bold text-lg dark:text-white">{{ entry.title }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ new Date(entry.entry_date).toLocaleString() }}</p>
                <p class="text-gray-700 dark:text-gray-300 text-sm mb-3">"{{ entry.content.substring(0, 200) }}..."</p>
                <div class="text-xs space-x-2">
                  <span v-for="emotion in entry.analyzed_emotions" :key="emotion" class="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 px-2 py-1 rounded-full">{{ emotion }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="activeTab === 'grafica'">
            <PieChartPatient :combination-data="emotionCombinations" />
          </div>

          <div v-else-if="activeTab === 'nube'">
            <WordCloudPatient :words="wordFrequency" />
          </div>
        </div>

        <div class="flex items-center justify-between bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mt-8">
    <div class="flex items-center space-x-3">
        <p class="text-sm text-gray-600 dark:text-gray-300">

            <span v-if="reportInfo?.is_available">
                El reporte semanal está listo para descargar.
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
        class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
        :disabled="isDownloading || !reportInfo?.is_available"
        :class="{ 'opacity-50 cursor-not-allowed': isDownloading || !reportInfo?.is_available }">
        {{ isDownloading ? 'Generando...' : 'Descargar PDF' }}
    </button>
</div>

      </div>
    </div>
  </div>

  <div v-if="showReportUnavailableModal" class="fixed inset-0 flex items-center justify-center z-50">
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

const patientId = route.params.id as string;

// --- LÓGICA COMPUTADA ---
const hasData = computed(() => diaryHistory.value.length > 0);

const tabClass = (tabName: 'historial' | 'grafica' | 'nube') => ({
  'py-2 px-4 text-lg font-medium transition-colors border-b-2': true,
  'text-blue-500 border-blue-500 dark:text-blue-400 dark:border-blue-400': activeTab.value === tabName,
  'text-gray-500 border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300': activeTab.value !== tabName,
});

// --- MÉTODOS DE ACCIÓN ---
function goBack() {
  router.back();
}

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

<style scoped>
/* Estilos necesarios para hacer que la tabla de info del paciente sea responsiva en móvil */
@media (max-width: 1023px) {
    .lg\:table { display: block; }
    .lg\:table-header-group { display: none; }

    .lg\:table-row {
        display: block;
        border: none !important;
        margin-bottom: 0.5rem;
        padding: 0;
        background: none !important;
        box-shadow: none !important;
    }

    .lg\:table-cell {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0;
        text-align: left !important;
        border-top: none !important;
    }

    .lg\:table-cell::before {
        content: attr(data-label) ":";
        font-weight: bold;
        display: block;
        color: #6b7280;
        flex-shrink: 0;
        margin-right: 1rem;
        width: 120px; /* Ancho fijo para la etiqueta en móvil */
    }

    .lg\:table-cell:first-child::before,
    .lg\:table-cell:last-child::before {
        display: none;
    }

    .lg\:table-cell:nth-child(1) { padding-top: 1rem; }
    .lg\:table-cell:nth-child(7) { padding-bottom: 1rem; }
    .lg\:table-cell > * {
        text-align: right;
        margin-left: auto;
    }
}
</style>
