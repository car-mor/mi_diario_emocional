<template>
    <div class="dark:bg-gray-800 transition-colors flex h-screen bg-gray-100">
        <Sidebar />
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-1">
            <StreakAndTitle title="Conferencia - TEDxTecdeMty" :streakCount="2" />
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        Salud mental, la clase que nadie nos dió.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Fernando Lemarroy</p>
                    <p class="text-sm text-gray-500">31 may 2022</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    “La salud mental no es un destino, sino un proceso - Noah Shpancer.”
                </p>
        
                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        Fernando nos enseña a cuidar nuestra salud mental y el empezar a ver por nuestro propio bienestar. <br></br>
                        Fernando es una persona que siempre ha sido muy inquieta desde pequeño, siempre ha sentido una especial curiosidad por hacer las cosas de otra manera, y buscar como trabajar con un equipo de personas con dotes comunicativas puede ser lo más efectivo del mundo.
                    </p>
                    <p class="mb-6 text-justify">
                        Actualmente es Co-fundador y Jefe de Oficina Operativa de The Startop, empresa dedicada a migrar negocios al mundo digital a través de estrategias de marketing con el objetivo de generar tráfico y aumentar las ventas. Fernando is a person who has always been very restless since he was little, he has always felt a special curiosity to do things differently, and looking for how to work with a team of people with communication skills can be the most effective thing in the world.
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 56.25%">
                            <iframe 
                                class="absolute top-0 left-0 w-full h-full rounded-2xl"
                                src="https://www.youtube.com/embed/_9agX3gY1jU?si=D_wsV1jekRcSt964" 
                                title="YouTube video player" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen>
                            </iframe>
                        </div>
                    </div>

                    <div class="mt-8 pt-4 border-t border-gray-200 text-gray-600 text-sm">
                    </div>
                </div>

                    <div class="mt-8 pt-4 border-t border-gray-200 text-gray-600 text-sm">
                        <h3 class="text-base font-bold text-gray-800 mb-2">Sobre él</h3>
                        <p class="mb-2">
                            **Fernando Lemarroy** 
                        </p>
                        <p class="text-xs text-gray-500">
                            **Fuente:** Adaptado de: #AprendemosJuntosBBVA2030. <br></br>
                            Ver más en: <a href="https://www.youtube.com/watch?v=S_0l-EqwknU" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">https://www.youtube.com/watch?v=S_0l-EqwknU</a>
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