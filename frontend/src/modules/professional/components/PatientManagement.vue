<template>
    <div class="p-6 dark:bg-gray-900">
        <div class="max-w-7xl mx-auto">
            
            <h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-8">Gestionar pacientes</h1>
            <!-- Mensaje cuando no hay pacientes vinculados -->
            <div v-if="patientList.length === 0" class="text-center p-12 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-inner">
                <p class="text-xl text-gray-600 dark:text-gray-300 font-medium leading-relaxed">
                    "No tienes pacientes vinculados actualmente. Comparte tu código de vinculación para que los pacientes puedan conectarse contigo."
                </p>
                <a href="/home-professional" class="mt-6 inline-block px-6 py-3 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold rounded-lg transition-colors duration-300 shadow-md">
                    Ver mi Código de Enlace
                </a>
            </div>
            <!-- Tabla de pacientes -->
            <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-xl">
                
                <div class="lg:overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700 lg:table">
                        
                        <thead class="bg-gray-50 dark:bg-gray-700 hidden lg:table-header-group">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">No.</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nombre</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Edad</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Género</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Correo electrónico</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Alias</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Avatar</th>
                                <th class="px-6 py-3 text-center text-xs font-bold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <!-- Cuerpo de la tabla -->
                        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                            <tr v-for="(patient, index) in patientList" :key="patient.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors block lg:table-row mb-4 lg:mb-0 p-4 lg:p-0 border border-gray-200 dark:border-gray-700 lg:border-none rounded-lg">
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white block lg:table-cell" data-label="No.">{{ index + 1 }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 block lg:table-cell font-semibold lg:font-normal" data-label="Nombre">{{ patient.name }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Edad">{{ patient.age }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Género">{{ patient.gender }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Correo electrónico">{{ patient.email }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 block lg:table-cell" data-label="Alias">{{ patient.alias }}</td>
                                
                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-sm text-gray-700 dark:text-gray-300 flex items-center justify-center" data-label="Avatar">
                                    <img 
                                        :src="patient.avatarUrl" 
                                        :alt="`Avatar de ${patient.alias}`"
                                        class="w-15 h-15 rounded-full object-cover border-2 border-blue-400"
                                    />
                                </td>

                                <td class="px-6 py-2 lg:py-4 whitespace-normal text-center text-sm font-medium block lg:table-cell" data-label="Acciones">
                                    <div class="flex items-center justify-center space-x-2 lg:justify-start">
                                        <button 
                                            @click="viewPatientDetails(patient.id)"
                                            class="p-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white transition-colors duration-200 shadow-md"
                                            title="Ver Detalles"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"></path><path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6"></path></svg>
                                        </button>

                                        <button 
                                            @click="openDisconnectModal(patient)"
                                            class="p-2 rounded-full bg-pink-500 hover:bg-pink-600 text-white transition-colors duration-200 shadow-md"
                                            title="Desvincular Paciente"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M18 6l-12 12"></path><path d="M6 6l12 12"></path></svg>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- Modal de confirmación para desvincular paciente -->
            <div v-if="showDisconnectModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-2xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white">Desvincular paciente</h3>
                    
                    <p v-if="selectedPatient" class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                        ¿Estás seguro de que deseas desvincular a <span class="font-semibold text-blue-600 dark:text-blue-400">[{{ selectedPatient.name }}]</span>? 
                        Esta acción no se puede deshacer y perderás acceso a toda la información de este paciente.
                    </p>
                    
                    <div class="flex justify-center space-x-4">
                        <button 
                            @click="showDisconnectModal = false" 
                            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg transition-colors"
                        >
                            Cancelar
                        </button>
                        <button 
                            @click="confirmDisconnect" 
                            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors"
                        >
                            Confirmar
                        </button>
                    </div>
                </div>
            </div>
            <!-- Modal de éxito tras desvinculación -->
            <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-2xl max-w-sm w-full text-center relative z-10 mx-4">
                    <h3 class="text-xl font-bold mb-4 dark:text-white text-green-600">¡Paciente Desvinculado!</h3>
                    
                    <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                        El paciente ha sido desvinculado de tu lista exitosamente.
                    </p>
                    
                    <button 
                        @click="showSuccessModal = false" 
                        class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full transition-colors"
                    >
                        Aceptar
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Definición de tipos para un paciente 
interface Patient {
    id: number;
    name: string;
    age: number;
    gender: 'Femenino' | 'Masculino' | 'Otro';
    email: string;
    alias: string;
    avatarUrl: string; 
}

// ----------------------------------------------------
// --- ESTADOS REACTIVOS Y DATOS DE PRUEBA
// ----------------------------------------------------

const patientList = ref<Patient[]>([
    { 
        id: 101, name: 'María Castañeda', age: 13, gender: 'Femenino', email: 'maria@correo.com', alias: 'xchmor',
        avatarUrl: 'https://i.pravatar.cc/150?img=1'
    },
    { 
        id: 102, name: 'Carlos López', age: 15, gender: 'Masculino', email: 'carlos@correo.com', alias: 'PsychoCat',
        avatarUrl: 'https://i.pravatar.cc/150?img=2'
    },
    { 
        id: 103, name: 'Juana Pérez', age: 16, gender: 'Femenino', email: 'juana@correo.com', alias: 'SweetPea',
        avatarUrl: 'https://i.pravatar.cc/150?img=3'
    },
    { 
        id: 104, name: 'Miguel Torres', age: 14, gender: 'Masculino', email: 'miguel@correo.com', alias: 'MigueT',
        avatarUrl: 'https://i.pravatar.cc/150?img=4'
    },
]);

//const patientList = ref<Patient[]>([]); // Lista vacía para probar el estado sin pacientes

const showDisconnectModal = ref(false);
const showSuccessModal = ref(false); 
const selectedPatient = ref<Patient | null>(null);

// ----------------------------------------------------
// --- MÉTODOS DE LA TABLA Y MODAL
// ----------------------------------------------------

function openDisconnectModal(patient: Patient) {
    selectedPatient.value = patient;
    showDisconnectModal.value = true;
}

function confirmDisconnect() {
    if (!selectedPatient.value) return;

    console.log(`[API CALL] Desvinculando paciente ID: ${selectedPatient.value.id}`);
    
    patientList.value = patientList.value.filter(
        p => p.id !== selectedPatient.value!.id
    );

    showDisconnectModal.value = false;
    showSuccessModal.value = true;
    
    console.log("¡Paciente desvinculado con éxito!");
}

function viewPatientDetails(patientId: number) {
    // ESTE ES EL CÓDIGO CORRECTO PARA ENVIAR EL ID:
    router.push({ name: 'PatientDetails', params: { id: patientId } });

    // Por ahora, solo mostramos una alerta y un log en consola
    alert(`ACCION: Navegando a la vista de detalles para el paciente ID: ${patientId}`);
    console.log(`Navegando a /patient/${patientId}`);
}

// Limpia el paciente seleccionado si el modal se cierra por cualquier razón.
watch(showDisconnectModal, (newVal) => {
    if (!newVal && selectedPatient.value) {
        selectedPatient.value = null;
    }
});
</script>

<style scoped>
/* Estilos para la responsividad de la tabla */
@media (max-width: 1023px) { /* Por debajo de lg (escritorio) */
    
    /* Hace que la tabla no actúe como tabla, sino como div/block */
    .lg\:table {
        display: block;
    }

    /* Oculta los encabezados de la tabla en móvil */
    .lg\:table-header-group {
        display: none;
    }

    /* Convierte cada fila de la tabla en una tarjeta (block) */
    .lg\:table-row {
        display: block;
        margin-bottom: 1rem; /* Espacio entre tarjetas */
        border: 1px solid #e5e7eb; /* Borde para la tarjeta */
        border-radius: 0.5rem; /* Bordes redondeados */
        background-color: white; /* Fondo de la tarjeta */
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    .dark .lg\:table-row {
        background-color: #1f2937; /* Fondo oscuro */
        border-color: #374151;
    }

    /* Convierte cada celda de la tabla en una fila de la tarjeta (flex para alineación) */
    .lg\:table-cell {
        display: flex; /* Usamos flex para alinear etiqueta y valor */
        justify-content: space-between; /* Etiqueta a la izquierda, valor a la derecha */
        align-items: center;
        padding: 0.5rem 1.5rem; /* Padding vertical y horizontal */
        text-align: left !important;
        border-top: 1px solid #f3f4f6; /* Separador entre ítems */
    }
    .dark .lg\:table-cell {
        border-color: #374151;
    }
    
    /* Agrega el label de la columna (ej: Nombre, Edad) y lo alinea a la izquierda */
    .lg\:table-cell::before {
        content: attr(data-label) ":"; /* Usa el atributo data-label del HTML y agrega dos puntos */
        font-weight: bold;
        display: block; /* Mantiene la etiqueta separada del valor */
        color: #6b7280; /* Color gris para el label */
        flex-shrink: 0; /* Evita que la etiqueta se encoja */
        margin-right: 1rem;
    }
    .dark .lg\:table-cell::before {
        color: #9ca3af;
    }

    /* Estilos para el VALOR (lo que está después de ::before) */
    .lg\:table-cell > * {
        flex-grow: 1; /* Permite que el contenido tome el espacio restante */
        text-align: right; /* Alinea el valor a la derecha de la tarjeta */
        margin-left: auto; /* Empuja el valor hacia la derecha */
    }

    /* Excepciones de alineación para la columna de acciones */
    .lg\:table-cell[data-label="Acciones"] > * {
        text-align: center;
    }

    /* Esconde el label de las celdas donde no lo necesitamos (ej: No. y Acciones) */
    .lg\:table-cell[data-label="No."]::before,
    .lg\:table-cell[data-label="Acciones"]::before {
        display: none; 
    }
}
</style>