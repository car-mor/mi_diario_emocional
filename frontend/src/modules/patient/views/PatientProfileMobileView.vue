<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo -->
        <Sidebar />
    
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- Encabezado con título y racha -->
            <StreakAndTitle title="Perfil del usuario" :streakCount="2" />

            <!-- Avatar -->
            <div class="mt-13 flex flex-col items-center text-center">
                <img
                    src="https://i.pravatar.cc/150?img=38"
                    alt="User avatar"
                    class="w-40 h-40 rounded-xl object-cover"
                />
                <h2 class="mt-3 text-lg font-semibold text-gray-800 dark:text-gray-200">
                    Alias de María
                </h2>
                <p class="text-sm text-gray-500">maria@correo.com</p>
            </div>

            <!-- Descripción -->
            <p class="ml-6 mr-6 text-center mt-4 text-sm text-gray-600 dark:text-gray-400 text-center">
            Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui. Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui.
            </p>

            <!-- Botón Configurar cuenta -->
            <div class="mt-6 flex flex-col gap-3 items-center">
                <button
                    type="submit"
                    class="w-60 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
                >
                    Configurar cuenta
                </button>

        <router-link
            to="/"
            class="w-60 sm:w-auto text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
        >
            Cerrar sesión
        </router-link>
</div>











    </main>


  </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import UserProfile from "../components/PatientProfile.vue"
</script>