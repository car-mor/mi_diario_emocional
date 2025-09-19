<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo component -->
        <Sidebar />
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle title="Nube de palabras de esta semana" :streakCount="2" />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        ¡Mira, esa nube tiene forma de estrella!
                    </h2>
                </div>


<div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
          En la sección de Nube de Palabras, podrás ver una recopilación de las palabras que más has ustilizado hasta ahora ¡Entre más grande la palabra más veces la has usado!
        </p>
                </div>


                <!-- Contenido principal - preguntas -->
                
                    <WordCloudPatient />
                

                

                <router-view /> 
            </div>
        </main>
        <!-- Perfil del usuario(solo en pantallas grandes) component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import UserProfile from "../components/PatientProfile.vue"
import WordCloudPatient from "../components/WordCloudPatient.vue"

</script>
