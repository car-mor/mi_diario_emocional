<template>
  <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6">
    <div class="flex items-center justify-between">
      <!-- Logo y título -->
      <div class="flex items-center space-x-3">
        <div class="flex items-center justify-center">
          <img src="@/assets/images/logo.png" alt="Logo <3" class="w-14 h-14 object-contain" />
        </div>
        <h1 class="text-xl font-semibold text-[#70BFE9]">Mi diario emocional</h1>
      </div>

      <!-- Navegación central -->
      <nav class="hidden md:flex items-center space-x-8">
        <a
          href="/home-professional"
          class="text-xl text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          Inicio
        </a>
        <a
          href="/patient-management"
          class="text-xl text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          Gestionar pacientes
        </a>
        <a
          href="/"
          class="text-xl text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          Cerrar sesión
        </a>
      </nav>

      <!-- Botones de la derecha -->
      <div class="flex items-center space-x-4 relative">
        <!-- Botón de tema -->
        <button
          @click="theme.toggleDark"
          class="rounded-full border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 px-4 py-1.5 text-lg font-medium text-gray-700 dark:text-gray-200 transition-all duration-200 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105"
        >
          {{ theme.isDark ? '🌙 ' : '☀️ ' }}
        </button>

        <!-- Botón Engrane Toggle -->
        <button
          @click="toggleSettingsMenu"
          :class="[
            'hidden sm:block p-2 rounded-full transition-all duration-200 hover:scale-105',
            showSettingsMenu 
              ? 'bg-[#70BFE9] text-white' 
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          ]"
        >
          <IconSettingsFilled 
            :class="[
              'w-8 h-8 transition-transform duration-200',
              showSettingsMenu ? 'rotate-45 text-white' : 'text-gray-600 dark:text-gray-300'
            ]" 
          />
        </button>

        <!-- Menú de configuración desplegable -->
        <div
          v-if="showSettingsMenu"
          class="absolute top-full right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50"
        >
          <div class="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-200">Soporte</h3>
          </div>
          
          <nav class="py-2">
            <a
              href="/faqs-tutorials-professional"
              class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
              @click="closeSettingsMenu"
            >
              <div class="flex items-center space-x-3">
                <IconZoomQuestion class="w-5 h-5" />
                <span>Preguntas frecuentes</span>
              </div>
            </a>
            
            <a
              href="/videos-tutorials-professional"
              class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
              @click="closeSettingsMenu"
            >
              <div class="flex items-center space-x-3">
                <IconVideo class="w-5 h-5" />
                <span>Video tutoriales</span>
              </div>
            </a>
            
          </nav>
        </div>
      </div>

      <!-- Menú móvil -->
      <div class="md:hidden">
        <button
          @click="toggleMobileMenu"
          class="p-2 rounded-md text-gray-600 rounded-full bg-gray-100 dark:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <IconMenu2 class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Menú móvil expandible -->
    <div
      v-if="showMobileMenu"
      class="md:hidden mt-4 pb-4 border-t border-gray-200 dark:border-gray-700 pt-4"
    >
      <nav class="flex flex-col space-y-4">
        <a
          href="/home-professional"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Inicio
        </a>
        <a
          href="/patient-management"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Gestionar pacientes
        </a>
        <a
          href="/videos-tutorials-professional"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Video tutoriales
        </a>
        <a
          href="/faqs-tutorials-professional"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Preguntas frecuentes
        </a>
        <a href="/">
            <button
            class="text-left text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
            >
                Cerrar sesión
            </button>
        </a>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// Importando solo los iconos de Tabler que necesitas
import { IconMenu2, IconSettingsFilled, IconZoomQuestion, IconVideo} from '@tabler/icons-vue'
import { useThemeStore } from '@/store/theme'

const theme = useThemeStore()

// Estados para los menús
const showMobileMenu = ref(false)
const showSettingsMenu = ref(false)

// Funciones para el menú móvil
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  // Cerrar menú de configuración si está abierto
  if (showMobileMenu.value) {
    showSettingsMenu.value = false
  }
}

// Funciones para el menú de configuración
const toggleSettingsMenu = () => {
  showSettingsMenu.value = !showSettingsMenu.value
  // Cerrar menú móvil si está abierto
  if (showSettingsMenu.value) {
    showMobileMenu.value = false
  }
}

const closeSettingsMenu = () => {
  showSettingsMenu.value = false
}
</script>