<template>
    <div class="dark:bg-gray-800 transition-colors flex h-screen bg-gray-100">
        <Sidebar />
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-1">
            <StreakAndTitle title="VIDEO - Mindfulness" :streakCount="2" />
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        Cómo Regular y Gestionar Emociones Con Mindfulness.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Helena Echeverría, psicóloga</p>
                    <p class="text-sm text-gray-500">12 may 2022</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    ““Hay que ser conscientes de que lo que nos provoca malestar o ansiedad no son los eventos, sino como vinculamos las emociones a éstos - Jonathan García-Allen. ”
                </p>
        
                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        El mindfulness es una práctica popular, pero… ¿sabes qué es mindfulness y para qué sirve? En esencia, se trata de una herramienta para alcanzar tu bienestar en medio del estrés diario. <br></br>
                        Conocida también como atención plena, la meditación mindfulness nos invita a concentrarnos en el momento presente a fin de mejorar nuestra conexión con nosotros mismos y con el entorno. Además de sus beneficios personales, ha demostrado ser un recurso efectivo en el ámbito educativo, especialmente para desarrollar habilidades cognitivas. <br></br>
                        Mindfulness en español es atención plena o conciencia plena. Esta traducción de mindfulness evidencia la idea de prestar atención de manera intencionada, sin distracciones y con aceptación. <br></br>
                        El significado de mindfulness se refiere a un estado mental en el que nos conectamos profundamente con el aquí y el ahora, dejando de lado juicios y preocupaciones. La conciencia plena se basa en observar pensamientos, sensaciones y emociones, sin aferrarnos a ellos.
                    </p>

                    <p class="mb-6 text-justify">
                        Aprende sobre emociones en este episodio. Descubre las emociones básicas que existen, cuáles son los componentes de una emoción y cómo gestionar emociones a través de un ejercicio práctico de mindfulness. ¡Adelante!
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 56.25%">
                            <iframe 
                                class="absolute top-0 left-0 w-full h-full rounded-2xl"
                                src="https://www.youtube.com/embed/RdAhXhP26Uo?si=fZZzIsgyUmSO-lun" 
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
                        <h3 class="text-base font-bold text-gray-800 mb-2">Sobre la especialista</h3>
                        <p class="mb-2">
                            **Helena Echeverría** Helena Echeverría es psicóloga, fundadora de PsicoGuías y autora de varios libros. S especializada en ansiedad, estrés y mindfulness, y es una de las voces más reconocidas en España sobre psicología positiva y desarrollo personal.
                        </p>
                        <p class="text-xs text-gray-500">
                            **Fuente:** Adaptado de: PsicoGuías | Podcast Psicología. <br></br>
                            Ver más en: <a href="https://www.youtube.com/watch?v=RdAhXhP26Uo" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">https://www.youtube.com/watch?v=RdAhXhP26Uo</a>
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