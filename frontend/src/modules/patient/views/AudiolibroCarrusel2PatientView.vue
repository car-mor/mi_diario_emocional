<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-12">
            <StreakAndTitle title="Audiolibro Completo" :streakCount="2" />

            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        Hábitos Atómicos.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Por James Clear</p>
                    <p class="text-sm text-gray-500">16 de octubre de 2018</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    “Un método sencillo y comprobado para desarrollar buenos hábitos y eliminar los malos.” 
                </p>

        
                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        HÁBITOS ATÓMICOS parte de una simple pero poderosa pregunta: ¿Cómo podemos vivir mejor? Sabemos que unos buenos hábitos nos permiten mejorar significativamente nuestra vida, pero con frecuencia nos desviamos del camino: dejamos de hacer ejercicio, comemos mal, dormimos poco, despilfarramos. ¿Por qué es tan fácil caer en los malos hábitos y tan complicado seguir los buenos?
                    </p>

                    <p class="mb-6 text-justify">
                        James Clear nos brinda fantásticas ideas basadas en investigaciones científicas, que le permiten revelarnos cómo podemos transformar pequeños hábitos cotidianos para cambiar nuestra vida y mejorarla. Esta guía pone al descubierto las fuerzas ocultas que moldean nuestro comportamiento
                        <br></br>—desde nuestra mentalidad, pasando por el ambiente y hasta la genética<br></br>— y nos demuestra cómo aplicar cada cambio a nuestra vida y a nuestro trabajo. 
                        Después de leer este libro, tendrás un método sencillo para desarrollar un sistema eficaz que te conducirá al éxito.
                    </p>

                    <p class="mb-6 text-justify">
                        Aprende cómo…
                        <br></br>• Darte tiempo para desarrollar nuevos hábitos
                        <br></br>• Superar la falta de motivación y de fuerza de voluntad
                        <br></br>• Diseñar un ambiente para que el éxito sea fácil de alcanzar
                        <br></br>• Regresar al buen camino cuando te hayas desviado un poco
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 5%">
                            <iframe 
                                style="border-radius:12px" 
                                src="https://open.spotify.com/embed/episode/5lS59Jy9mZHvkuAzYUrvnW?utm_source=generator" 
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
                        <h3 class="text-base font-bold text-gray-800 mb-2">Sobre el autor</h3>
                        <p class="mb-2">
                            **James Clear** Clear se graduó en Denison y comenzó su carrera como entrenador de rendimiento para atletas y ejecutivos. Luego se dedicó a escribir y a hablar en público. En 2012, comenzó a escribir sobre superación personal presentando su libro Hábitos Atómicos. Su trabajo también ha aparecido en The New York Times, Forbes y Time.
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