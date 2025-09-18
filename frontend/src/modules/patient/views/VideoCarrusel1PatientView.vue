<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-12">
            <StreakAndTitle title="VIDEO - Aprendemos Juntos BBVA" :streakCount="2" />
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        V. Completa. Recupera tu mente, reconquista tu vida.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Marian Rojas-Estapé, psiquiatra y escritora</p>
                    <p class="text-sm text-gray-500">22 jul 2024</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    “¿Se puede educar el optimismo? “Sí, se puede aprender a ser optimista”. Y depende de nuestra voz interior, de cómo vemos la realidad y de si estamos dispuestos a conectar con el presente y profundizar en la trascendencia de la vida más allá de las pantallas, la superficialidad y las adicciones. Para la psiquiatra y experta en neurociencia Marian Rojas-Estapé técnicas como la contemplación y la instrospección nos permitirán ver lo que hay dentro de nosotros mismos y fuera con ojos nuevos, y a conectar con las pequeñas alegrías del día a día. En este vídeo, la reconocida psiquiatra y experta en neurociencia explica cómo la comprensión del funcionamiento de nuestro cerebro, nuestras emociones y nuestro organismo nos ayuda a vivir una vida más real: “Nuestra voz interior influye en el sistema inmune y cuando comprendes por lo que pasa tu mente, te sientes aliviado; porque si no eres esclavo de síntomas físicos, psicológicos y vas perdido por la vida”. 
                </p>
        
                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        Cuando Rojas-Estapé comenzó a estudiar Medicina sentía que siempre faltaba el plano emocional en el abordaje de las enfermedades, siendo reconocida por su enfoque humanista en la conexión de la salud física y mental con la somatización emocional. Marian es una de las psiquiatras más influyentes de la actualidad por su capacidad para explicar conceptos complejos de manera accesible, ayudando a muchas personas a conocerse y a gestionar de manera más consciente sus emociones. “Entender que la mente, el cuerpo y el alma están profundamente unidos es fundamental a la hora de abordar una terapia pero no patologicemos todo lo que nos sucede. No todo tiene que ser paliado con medicación y no todo tiene que ser tratado por un profesional. Hay procesos que cada cual tiene que vivir a medida que nos van sucediendo”, reflexiona. 
                    </p>

                    <p class="mb-6 text-justify">
                        Marian Rojas-Estapé es psiquiatra licenciada en Medicina y Cirugía por la Universidad de Navarra, y compagina su trabajo en el Instituto Español de Investigaciones Psiquiátricas con su labor como colaboradora en universidades, proyectos de cooperación, divulgadora y autora de obras superventas como ‘Cómo hacer que te pasen cosas buenas’, ‘Encuentra tu persona vitamina’, y ‘Recupera tu mente, reconquista tu vida’. Su último trabajo, en el que pone de relieve la urgencia de profundizar en nuestras vidas para saber elegir, identificar patrones y alejarnos del mundanal ruido para proteger nuestra salud física y psicológica.
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 56.25%">
                            <iframe 
                                class="absolute top-0 left-0 w-full h-full rounded-2xl"
                                src="https://www.youtube.com/embed/S_0l-EqwknU?si=R_LydyDwWWnhnEfo" 
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
                            **Marian Rojas-Estapé** Marian Rojas Estapé es una médica, especialista en psiquiatría y escritora española. Su padre es el psiquiatra y escritor Enrique Rojas y su madre la notaria y profesora universitaria Isabel Estapé. Es nieta del economista Fabián Estapé. Comenzó la Licenciatura de Medicina en la Universidad Complutense de Madrid, concluyéndola en la Universidad de Navarra (2007). Concluida la licenciatura, se especializó en Psiquiatría.
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