<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-12">
            <StreakAndTitle title="Podcast - Vamos a Meditar" :streakCount="2" />
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        Ejercicio de Respiración para calmar la ansiedad.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Por Glenda Yoga</p>
                    <p class="text-sm text-gray-500">16 de noviembre 2018</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    “Toma un momento para calmar tu mente, regálate unos minutos, libera tensiones, duerme mejor.”. 
                </p>
        
                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        ¿Sabías que tan sólo con respirar de manera adecuada puedes bajar la ansiedad y el estrés? En este podcast te guiaré en un ejercicio de respiración consciente que puedes hacer en cualquier momento del día para calmar tu mente y cuerpo. La respiración es una herramienta poderosa que todos tenemos a nuestro alcance, y aprender a utilizarla correctamente puede mejorar significativamente tu bienestar emocional y físico.
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 5%">
                            <iframe 
                                style="border-radius:12px" 
                                src="https://open.spotify.com/embed/episode/5kVQKI7fpewVRVzEnOFxoM?utm_source=generator" 
                                width="100%" 
                                height="352" 
                                frameBorder="0" 
                                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                                loading="lazy">
                            </iframe>
                        </div>
                    </div>

                    <div class="mt-8 pt-4 border-t border-gray-200 text-gray-600 text-sm">
                    </div>
                </div>

                    <div class="mt-8 pt-4 border-t border-gray-200 text-gray-600 text-sm">
                        <h3 class="text-base font-bold text-gray-800 mb-2">Sobre la instructora</h3>
                        <p class="mb-2">
                            **Glenda Yoga** Practicante de Yoga desde el 2012, estudios en India, practica la meditación Vipassana desde hace varios años.
                        </p>
                        <p class="text-xs text-gray-500">
                            **Fuente:** Adaptado de: #Spotify. <br></br>
                        </p>
                    </div>
                </div>
            </div>
        <router-view />
        </main>

        <UserProfile />
    </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue";
import StreakAndTitle from "../components/StreakAndTitlePatient.vue";
import UserProfile from "../components/PatientProfile.vue";
</script>