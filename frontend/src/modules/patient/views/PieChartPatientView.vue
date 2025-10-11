<template>
    <div class="flex h-screen">

        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle title="Gráfico de pastel de esta semana" :streakCount="2" />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Mi análisis de emociones de esta semana
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En esta sección podrás ver una gráfica de tu análisis de emociones hasta ahora, se muestran las 5 combinaciones de emociones más frecuentes que has experimentado basándote en tus entradas del diario de esta semana.
                    </p>
                </div>
                <!-- Contenido principal - component gráfico de pastel -->
                <PieChart />
                <router-view />
            </div>
        </main>
        <!-- Perfil del usuario component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
    import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
    import UserProfile from "../components/PatientProfile.vue"
    import PieChart from "../components/PieChartPatient.vue"
</script>
