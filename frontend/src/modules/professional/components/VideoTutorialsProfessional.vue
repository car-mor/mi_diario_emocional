<template>
    <div class="flex">
        <main class="flex-1 flex flex-col overflow-hidden">
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">    
                <div class="p-4 flex flex-col text-left">
                    <div class="flex items-center justify-start mb-4">
                        <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-200 ml-4">
                            Video Tutoriales
                        </h2>
                    </div>
                    </div>
                <div class="max-w-3xl mx-auto px-4">
                    <h2 class="text font-semibold text-gray-800 dark:text-gray-200 mb-6">Te mostramos la Lista de Tutoriales</h2>
                    
                    <div class="space-y-6">
                        <div
                            v-for="(video, index) in videoItems"
                            :key="index"
                            class="bg-white rounded-lg shadow-md overflow-hidden dark:text-white dark:bg-gray-800"
                        >
                            <button
                                @click="toggleVideo(index)"
                                class="w-full flex items-center p-4 text-left font-semibold text-lg text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" :class="['w-6 h-6 mr-3 transition-transform', openVideoIndex === index ? 'rotate-180 text-[#70BFE9]' : 'text-gray-400']" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M6 9l6 6l6 -6"></path></svg>
                                
                                <span>{{ video.title }}</span>
                            </button>

                            <div
                                v-if="openVideoIndex === index"
                                class="p-4 bg-gray-50 border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600"
                            >
                                <div class="relative w-full aspect-video">
                                    <iframe 
                                        :src="video.src" 
                                        frameborder="0" 
                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                        allowfullscreen
                                        class="absolute inset-0 w-full h-full rounded-lg shadow-xl"
                                        title="Video Tutorial"
                                    ></iframe>
                                </div>
                                <p v-if="video.description" class="mt-4 text-gray-700 dark:text-gray-300">{{ video.description }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <router-view /> 
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Lógica de Videos Tutoriales
const openVideoIndex = ref<number | null>(null);
const videoItems = [
    {
        title: 'Introducción a la plataforma y primeros pasos',
        description: 'Aprende a navegar por la interfaz y configura tu perfil profesional en menos de 5 minutos.',
        // URL de YouTube (ejemplo: reemplazar con tu ID de video real)
        src: 'https://www.youtube.com/embed/IzZ3VCQKDl0?si=Zc9JZHd-qRNu9yHb',
    },
    {
        title: 'Gestión de pacientes: Enlace y seguimiento',
        description: 'Descubre cómo compartir tu código de enlace y monitorear el progreso emocional de tus pacientes.',
        src: 'https://www.youtube.com/embed/IzZ3VCQKDl0?si=Zc9JZHd-qRNu9yHb',
    },
    {
        title: 'Análisis de datos y reportes emocionales',
        description: 'Tutorial avanzado para interpretar los datos combinados y generar reportes útiles para tus sesiones.',
        src: 'https://www.youtube.com/embed/IzZ3VCQKDl0?si=Zc9JZHd-qRNu9yHb',
    },
];

const toggleVideo = (index: number) => {
    // Abre el video si está cerrado, o lo cierra si está abierto.
    openVideoIndex.value = openVideoIndex.value === index ? null : index;
}

</script>