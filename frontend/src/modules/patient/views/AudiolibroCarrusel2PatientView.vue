<template>
    <div class="dark:bg-gray-800 transition-colors flex h-screen bg-gray-100">
        <main class="flex-1 flex flex-col overflow-y-auto p-8 lg:p-1">
            <StreakAndTitle title="Audiolibro Completo" :streakCount="2" />

            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-10 lg:p-16 max-w-4xl mx-auto my-6">
                <div class="text-center mb-8">
                    <h1 class="text-3xl md:text-4xl font-bold text-gray-800 leading-tight mb-2">
                        Los Cuatro Acuerdos.
                    </h1>
                    <p class="text-lg text-gray-600 font-semibold">Por Don Miguel Ruiz</p>
                    <p class="text-sm text-gray-500">26 de abril de 2022</p>
                </div>

                <p class="text-xl md:text-2xl font-light text-gray-700 italic text-center leading-relaxed mb-8">
                    “Una guía práctica para la libertad personal basada en la sabiduría tolteca.”
                </p>


                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <p class="mb-6 text-justify">
                        En <strong>Los Cuatro Acuerdos</strong>, Don Miguel Ruiz revela la fuente de las creencias limitantes que nos roban la alegría y crean un sufrimiento innecesario. Basado en la antigua sabiduría tolteca, este libro ofrece un poderoso código de conducta que puede transformar rápidamente nuestras vidas en una nueva experiencia de libertad, verdadera felicidad y amor.
                      </p>

                    <p class="mb-6 text-justify">
                        El autor nos guía para romper los "acuerdos" autodestructivos que hemos hecho con nosotros mismos, impuestos por el miedo y la "domesticación" social. Estos acuerdos son la causa de nuestro sufrimiento y nos impiden ver quiénes somos realmente.
                        <br></br>
                        Al adoptar y vivir según los Cuatro Acuerdos, podemos liberarnos del auto-juicio, la culpa y la vergüenza, y comenzar a vivir una vida basada en el amor propio y la aceptación.
                    </p>

                    <p class="mb-6 text-justify">
                        Los Cuatro Acuerdos son:
                        <br></br>• <strong>Sé impecable con tus palabras:</strong> Habla con integridad y evita usar la palabra contra ti mismo (chismes, autocrítica).
                        <br></br>• <strong>No te tomes nada personalmente:</strong> Lo que otros dicen y hacen es una proyección de su propia realidad, no una verdad sobre ti.
                        <br></br>• <strong>No hagas suposiciones:</strong> Encuentra la valentía para preguntar y comunicar con claridad, evitando malentendidos y drama.
                        <br></br>• <strong>Haz siempre lo máximo que puedas:</strong> Tu máximo esfuerzo variará (si estás enfermo o sano), pero si siempre haces lo mejor, evitarás el auto-juicio.
                    </p>

                <div class="text-gray-700 leading-relaxed text-base md:text-lg">
                    <div class="mb-8">
                        <div class="relative overflow-hidden w-full" style="padding-top: 5%">
                            <iframe
                                style="border-radius:12px"
                                src="https://open.spotify.com/embed/episode/2jOKKFrRDPXbpZ6WJnlL3N?utm_source=generator"
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
                            **Don Miguel Ruiz** es un autor mexicano, chamán (nagual) y maestro de la tradición tolteca. Nació en una familia de curanderos y creció en el México rural. Aunque estudió medicina y se convirtió en cirujano, una experiencia cercana a la muerte lo llevó a redescubrir la sabiduría ancestral de su familia, dedicándose a compartir las enseñanzas toltecas con el mundo.
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
import StreakAndTitle from "../components/StreakAndTitlePatient.vue";
import UserProfile from "../components/PatientProfile.vue";
</script>
