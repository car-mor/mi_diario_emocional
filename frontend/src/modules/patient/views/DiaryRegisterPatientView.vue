<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo component -->
        <Sidebar />
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle title="¡Este es tu diario de emociones! :)" :streakCount="2" />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Hoy es un buen día para escribir en tu diario
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En esta sección puedes registrar tus emociones y pensamientos diarios. Recuerda que expresar lo que sientes puede ayudarte a comprenderte mejor y a manejar tus emociones de manera saludable.
                    </p>
                </div>
                <!-- Contenido principal - component  -->
                <DiaryRegister />
                <router-view /> 
            </div>
        </main>
        <!-- Perfil del usuario component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
    import Sidebar from "../components/SidebarPatient.vue"
    import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
    import UserProfile from "../components/PatientProfile.vue"
    import DiaryRegister from "../components/DiaryRegister.vue"
</script>
