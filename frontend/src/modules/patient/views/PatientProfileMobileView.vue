<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo -->
        <Sidebar />
    
        <!-- Área principal central -->
        <main class="dark:bg-gray-800 flex-1 flex flex-col overflow-hidden">
            <!-- Encabezado con título y racha -->
            <StreakAndTitle title="Perfil del usuario" :streakCount="2" />
            
            <!-- Perfil del usuario(solo en pantallas moviles) -->
            <PatientProfileMobile />
        </main>
    </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import PatientProfileMobile from "../components/PatientProfileMobile.vue";
</script>