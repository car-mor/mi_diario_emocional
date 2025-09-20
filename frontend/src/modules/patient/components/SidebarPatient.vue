<template>
    <div>
        <!-- Botón menú hamburguesa (solo en móvil, fijo arriba a la izquierda color azul) -->
        <button
            @click="toggleMobileMenu"
            class="md:hidden fixed top-4 left-4 z-50 p-2 rounded-full bg-[#7DBFF8] text-white shadow-lg"
        >
        <IconMenu2 class="w-6 h-6" />
        </button>

    <!-- Sidebar -->
    <aside
    :class="[
        'dark:bg-gray-900 transition-colors fixed md:static top-0 left-0 h-full w-18 bg-[#7DBFF8] text-white flex flex-col items-center py-6 transform transition-transform duration-300 z-40 overflow-y-auto',
        showMobileMenu ? 'translate-x-0' : '-translate-x-full',
        'md:translate-x-0 md:w-15 lg:w-24'
    ]"
    >
        <!-- Navegación -->
        <nav class="flex flex-col space-y-4 md:space-y-6 flex-1 mt-12 md:mt-6 min-h-0 justify-center md:justify-start">
            <!-- Icono Perfil (solo en móvil) -->
            <router-link
                to="/profile-patient-mobile"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0 block md:hidden"
            >
                <IconUserCircle class="w-8 h-8" />
            </router-link>
            <!-- Icono Home -->
            <router-link
                to="/home-patient"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconHome class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono Diario -->
            <router-link
                to="/library"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconBook class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono Historial -->
            <router-link
                to="/history"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconClock class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono Gráfica de Pastel -->
            <router-link
                to="/pie-chart-patient"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconChartPie2 class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono Nube de Palabras -->
            <router-link
                to="/word-cloud-patient"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconCloud class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono FAQs -->
            <router-link
                to="/faqs-patient"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconHelpHexagon class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
            <!-- Icono Configuración -->
            <router-link
                to="/faq"
                class="flex justify-center p-2 md:p-3 rounded-full hover:bg-[#5aa7d1] transition flex-shrink-0"
            >
                <IconSettings class="w-8 h-8 md:w-10 md:h-10" />
            </router-link>
        </nav> 
    </aside>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { IconHome, IconMenu2, IconBook, IconClock, IconChartPie2, IconCloud, IconHelpHexagon, IconSettings, IconUserCircle } from "@tabler/icons-vue"

const showMobileMenu = ref(false)
const toggleMobileMenu = () => {
    showMobileMenu.value = !showMobileMenu.value
}
</script>