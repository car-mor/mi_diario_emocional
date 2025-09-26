<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo component -->
        <Sidebar />
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle title="Ajustes y configuraciones de la cuenta" :streakCount="2" />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Ajustes y Configuraciones
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En esta sección puedes ajustar la configuración de tu cuenta. Asegúrate de que toda tu información esté actualizada para mejorar tu experiencia.
                    </p>
                </div>
                <!-- Contenido principal - component  -->
                <AccountSettings />
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
    import AccountSettings from "../components/PatientAccountSettings.vue"
</script>
