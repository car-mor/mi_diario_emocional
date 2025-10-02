<template>
    <div class="p-6 dark:bg-gray-900 min-h-screen">
        <div class="max-w-7xl mx-auto">
            
            <div class="flex items-center justify-between mb-8">
                <button 
                    @click="goBack" 
                    class="p-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-800 dark:text-white" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15 6l-6 6l6 6"></path></svg>
                </button>
                <h1 class="text-3xl font-bold text-gray-800 dark:text-white flex-grow text-center lg:text-left ml-4">
                    Paciente: {{ patient.name }}
                </h1>
            </div>

            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 mb-8">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700 lg:table">
                        <thead class="bg-gray-50 dark:bg-gray-700 hidden lg:table-header-group">
                            <tr>
                                <th v-for="header in patientHeaders" :key="header" class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">{{ header }}</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                            <tr class="block lg:table-row p-4 lg:p-0 border-b dark:border-gray-700">
                                <td class="px-6 py-2 lg:py-4 text-sm font-medium text-gray-900 dark:text-white block lg:table-cell" data-label="No.">1</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell font-semibold lg:font-normal" data-label="Nombre">{{ patient.name }}</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Edad">{{ patient.age }}</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Género">{{ patient.gender }}</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Correo electrónico">{{ patient.email }}</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Alias">{{ patient.alias }}</td>
                                <td class="px-6 py-2 lg:py-4 text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Avatar">
                                    <img :src="patient.avatarUrl" :alt="`Avatar de ${patient.alias}`" class="w-10 h-10 rounded-full object-cover border-2 border-blue-400" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <h2 class="text-2xl font-bold text-gray-800 dark:text-white mt-8 mb-4">Análisis Semanal</h2>
            
            <div class="flex border-b border-gray-300 dark:border-gray-700 mb-6">
                <button
                    @click="activeTab = 'historial'"
                    :class="tabClass('historial')"
                >Historial de escritos</button>
                <button
                    @click="activeTab = 'grafica'"
                    :class="tabClass('grafica')"
                >Gráfica de pastel</button>
                <button
                    @click="activeTab = 'nube'"
                    :class="tabClass('nube')"
                >Nube de palabras</button>
            </div>

            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 min-h-[500px]">
                
                <div v-if="activeTab === 'historial'">
                    <div v-if="!hasData" class="flex justify-center items-center h-[400px]">
                        <p class="text-xl text-gray-600 dark:text-gray-300">No hay escritos recientes para mostrar.</p>
                    </div>
                    <div v-else class="space-y-6">
                        <div v-for="(escrito, index) in patientData.historial" :key="index" class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 grid grid-cols-1 md:grid-cols-3 gap-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                            <div class="md:col-span-1 border-r pr-4 dark:border-gray-600">
                                <span class="text-4xl font-light text-gray-400 dark:text-gray-500 mr-4">{{ escrito.no }}.</span>
                                <p class="text-md font-semibold text-gray-800 dark:text-white mb-2">{{ escrito.titulo }}</p>
                                <p class="text-sm text-gray-600 dark:text-gray-300 italic">{{ escrito.texto }}</p>
                            </div>
                            <div class="md:col-span-1 border-r pr-4 dark:border-gray-600">
                                <p class="text-md font-semibold text-gray-800 dark:text-white mb-2">Emociones básicas de Ekman</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400">{{ escrito.emocionesBasicas }}</p>
                            </div>
                            <div class="md:col-span-1">
                                <p class="text-md font-semibold text-gray-800 dark:text-white mb-2">Análisis emociones combinadas</p>
                                <ul class="text-sm text-gray-600 dark:text-gray-300 space-y-1">
                                    <li v-for="(analisis, i) in escrito.analisisCombinado" :key="i">{{ analisis }}</li>
                                </ul>
                                <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 text-right">{{ escrito.fecha }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else-if="activeTab === 'grafica'">
                    <div v-if="!hasData" class="flex flex-col justify-center items-center h-[400px] text-center">
                        <p class="text-xl font-bold text-gray-800 dark:text-white mb-4">No hay suficientes datos para generar esta visualización.</p>
                        <p class="text-gray-600 dark:text-gray-300">¡Oops! Parece que tu paciente aún no ha escrito nada en su diario, esperemos a que lo haga.</p>
                    </div>
                    <div v-else class="grid lg:grid-cols-2 gap-8 items-center">
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Porcentajes de emociones combinadas</h3>
                            <p class="text-gray-600 dark:text-gray-300 mb-6">Se muestran las emociones combinadas de la última semana.</p>
                            <div class="relative w-full h-80">
                                <img :src="donutChart" alt="Gráfica de Pastel de Emociones Combinadas" class="w-full h-full object-contain mx-auto" />
                            </div>
                        </div>
                        <div class="space-y-3">
                            <div v-for="(item, index) in patientData.grafica.legend" :key="index" class="flex items-center">
                                <span :style="{ backgroundColor: item.color }" class="w-4 h-4 rounded-full mr-3"></span>
                                <span class="text-gray-700 dark:text-gray-300 text-sm">{{ item.label }}</span>
                                <span class="ml-auto text-sm font-semibold" :style="{ color: item.color }">{{ item.percent }}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else-if="activeTab === 'nube'">
                    <div v-if="!hasData" class="flex flex-col justify-center items-center h-[400px] text-center">
                        <p class="text-xl font-bold text-gray-800 dark:text-white mb-4">No hay suficientes datos para generar esta visualización.</p>
                        <p class="text-gray-600 dark:text-gray-300">¡Oops! Parece que tu paciente aún no ha escrito nada en su diario, esperemos a que lo haga.</p>
                    </div>
                    <div v-else class="grid lg:grid-cols-2 gap-8 items-center">
                        <div class="lg:col-span-2">
                            <h3 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Nube de palabras</h3>
                            <p class="text-gray-600 dark:text-gray-300 mb-6">Esta Nube de Palabras muestra las palabras más frecuentes. Entre más grande es la palabra, más frecuente es.</p>
                        </div>
                        
                        <div class="relative w-full h-auto">
                            <img :src="wordCloud" alt="Nube de Palabras" class="w-full h-full object-contain mx-auto" />
                        </div>
                        
                        <div class="pl-4">
                            <ol class="list-none space-y-1 text-gray-700 dark:text-gray-300 text-lg font-medium">
                                <li v-for="(word, index) in patientData.nube.frecuentes" :key="index">
                                    {{ index + 1 }}. {{ word }}
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>

            </div>

            <div class="flex items-center justify-between bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mt-8">
                <div class="flex items-center space-x-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-500 dark:text-gray-400" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 21a9 9 0 0 1 -9 -9a9 9 0 0 1 9 -9a9 9 0 0 1 9 9a9 9 0 0 1 -9 9z"></path><path d="M12 14l0 4"></path><path d="M12 8l0 4"></path></svg>
                    <p class="text-sm text-gray-600 dark:text-gray-300">
                        El reporte en PDF de esta semana se generará el: <span class="font-semibold">{{ reportDate }}</span>
                    </p>
                </div>
                <button 
                    @click="downloadPdf"
                    class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors duration-300"
                >
                    Descargar PDF
                </button>
            </div>

        </div>

        <div v-if="showReportUnavailableModal" class="fixed inset-0 flex items-center justify-center z-50">
            <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-2xl max-w-sm w-full text-center relative z-10 mx-4">
                <h3 class="text-xl font-bold mb-4 dark:text-white">Aviso</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                    Aún no se cumple la primera semana para descargar el reporte de análisis emocional. El primer reporte estará disponible a partir de [{{ reportDate }}].
                </p>
                <button @click="showReportUnavailableModal = false" class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold w-full">Aceptar</button>
            </div>
        </div>

        <div v-if="showDownloadSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
            <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-2xl max-w-sm w-full text-center relative z-10 mx-4">
                <div class="w-16 h-16 mx-auto bg-green-500 rounded-full flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-white" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M5 12l5 5l10 -10"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-4 dark:text-white">¡Descarga Exitosa!</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                    El reporte PDF de esta semana se generó correctamente.
                </p>
                <button @click="showDownloadSuccessModal = false" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-semibold w-full">Entendido</button>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
// NOTE: Asumiendo que esta es una vista enrutada y que el ID del paciente se pasa por parámetros.

// --- Definición de Tipos ---
interface PatientInfo {
    id: number;
    name: string;
    age: number;
    gender: string;
    email: string;
    alias: string;
    avatarUrl: string;
}

interface Escrito {
    no: number;
    titulo: string;
    texto: string;
    emocionesBasicas: string;
    analisisCombinado: string[];
    fecha: string;
}

interface PatientAnalysisData {
    hasData: boolean;
    reportAvailable: boolean; // Simula si ha pasado una semana
    
    historial: Escrito[];
    
    grafica: {
        data: any; // Aquí iría la estructura de datos del gráfico (por simplicidad, solo usamos la leyenda)
        legend: { color: string; label: string; percent: number; }[];
    };
    
    nube: {
        frecuentes: string[];
    };
}


// --- ESTADOS DE PÁGINA ---
const activeTab = ref<'historial' | 'grafica' | 'nube'>('historial');
const showReportUnavailableModal = ref(false);
const showDownloadSuccessModal = ref(false);
const showNoDataModal = ref(false); // Modal de "No hay suficientes datos"

// --- DATOS SIMULADOS ---

// 1. Datos del Paciente (Se cargaría del ID en la URL)
const patient = ref<PatientInfo>({
    id: 101,
    name: 'Maria Castañeda',
    age: 13,
    gender: 'Femenino',
    email: 'maria@correo.com',
    alias: 'xchmor',
    avatarUrl: 'https://i.pravatar.cc/150?img=1',
});

// 2. Fecha del Reporte (Simulación)
const reportDate = ref('28 de Septiembre 2025');

// 3. Imágenes de las Visualizaciones (Rutas de las imágenes subidas)
const donutChart = ref('src/assets/images/grafica-de-pastel.png'); 
const wordCloud = ref('src/assets/images/Nube-de-palabras.png');


// 4. Datos de Análisis del Paciente (Se cargarían del backend)
const patientData = ref<PatientAnalysisData>({
    hasData: true,
    reportAvailable: true, 

    historial: [
        {
            no: 1,
            titulo: 'Neque porro quisquam est qui dolorem ipsum quia',
            texto: '"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...."',
            emocionesBasicas: 'Alegría, Asco',
            analisisCombinado: ['20% Alegría y tristeza', '15% Enojo y tristeza', '65% Nostalgia y tristeza'],
            fecha: '3 de Agosto 2022 23:23'
        },
         {
            no: 2,
            titulo: 'Neque porro quisquam est qui dolorem ipsum quia',
            texto: '"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...."',
            emocionesBasicas: 'Alegría, Asco',
            analisisCombinado: ['20% Alegría y tristeza', '15% Enojo y tristeza', '65% Nostalgia y tristeza'],
            fecha: '3 de Agosto 2022 23:23'
        },
    ],
    
    grafica: {
        data: [], // null - Para simular que el gráfico está cargado
        legend: [
            { color: '#FFD700', label: 'Alegría, miedo', percent: 40 },
            { color: '#CD5C5C', label: 'Asco, ira', percent: 30 },
            { color: '#4682B4', label: 'Tristeza, alegría', percent: 10 },
            { color: '#8FBC8F', label: 'Asco, miedo, ira, sorpresa', percent: 5 },
            { color: '#6A5ACD', label: 'Sorpresa, miedo, tristeza', percent: 15 },
        ],
    },
    
    nube: {
        frecuentes: ['Cansada', 'Escuela', 'Navidad', 'Casa', 'Amigos', 'Maria'],
    },
});

// --- LÓGICA COMPUTADA ---

const hasData = computed(() => patientData.value.hasData);

const tabClass = (tabName: 'historial' | 'grafica' | 'nube') => ({
    'py-2 px-4 text-lg font-medium transition-colors border-b-2': true,
    'text-blue-500 border-blue-500 dark:text-blue-400 dark:border-blue-400': activeTab.value === tabName,
    'text-gray-500 border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300': activeTab.value !== tabName,
});

const patientHeaders = ['No.', 'Nombre', 'Edad', 'Género', 'Correo electrónico', 'Alias', 'Avatar'];


// --- MÉTODOS DE ACCIÓN ---

function goBack() {
    // Aquí iría: router.go(-1) o router.push('/manage-patients')
    alert("Simulación de regreso a Gestionar Pacientes.");
}

function downloadPdf() {
    if (!patientData.value.reportAvailable) {
        // Mostrar modal de aviso si no ha pasado una semana
        showReportUnavailableModal.value = true;
        return;
    }
    
    // Simular la llamada a la API para generar/descargar el PDF
    console.log("Generando y descargando PDF...");
    
    // Simular éxito y mostrar modal
    setTimeout(() => {
        showDownloadSuccessModal.value = true;
    }, 500);
}


// --- CARGA DE DATOS AL INICIO ---
onMounted(() => {
    

    // Aquí se haría la llamada real al backend para cargar los datos del paciente y su análisis
    // Por simplicidad, usamos los datos simulados definidos arriba.
});

// Manejo de clicks en el contenido para mostrar modales de datos insuficientes
// Esto se haría idealmente en el backend, pero aquí forzamos la lógica del modal de "No hay datos"
const checkDataAndSetTab = (tabName: 'historial' | 'grafica' | 'nube') => {
    if (!hasData.value) {
        // Forzamos el modal de "No hay suficientes datos" si el paciente no tiene data
        // Esto solo ocurre si patientData.value.hasData es false.
        showNoDataModal.value = true; 
        return;
    }
    activeTab.value = tabName;
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