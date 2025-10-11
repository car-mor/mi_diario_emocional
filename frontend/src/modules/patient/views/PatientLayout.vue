<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo component -->

        <Sidebar />
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle title="Soporte y FAQs" :streakCount="2" />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <router-view />
            </div>
        </main>
        <!-- Perfil del usuario(solo en pantallas grandes) component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
</script>
