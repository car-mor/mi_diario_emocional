<template>
  <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6">
    <div class="flex items-center justify-between">
      <!-- Logo y título -->
      <a href="/">
      <div class="flex items-center space-x-3">

        <div class="flex items-center justify-center">
          <img
    src="/images/logo.png"
    alt="Logo Mi Diario Emocional"
    class="w-14 h-14 object-contain"
  />
        </div>
        <h1 class="text-xl font-semibold text-[#70BFE9]">Mi diario emocional</h1>
      </div>
      </a>

      <!-- Navegación central -->
      <nav class="hidden md:flex items-center space-x-8">
        <a
          href="/faq"
          class="text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          Preguntas frecuentes
        </a>
        <a
          href="/who-are-we"
          class="text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          ¿Quiénes somos?
        </a>
        <a
          href="/data-protection"
          class="text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-[#70BFE9] font-medium transition-colors duration-200"
        >
          ¿Cómo protegemos los datos?
        </a>
      </nav>

      <!-- Botones de la derecha -->
      <div class="flex items-center space-x-4">
        <!-- Botón de tema -->
        <button
          @click="theme.toggleDark"
          class="rounded-full border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 px-4 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-200 transition-all duration-200 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105"
        >
          {{ theme.isDark ? '🌙 ' : '☀️ ' }}
        </button>

        <!-- Botón Iniciar sesión -->
        <router-link
          to="/login"
          class="text-gray-700 dark:text-gray-200 hover:text-[#70BFE9] dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Iniciar sesión
        </router-link>

        <!-- Botón Home -->
        <router-link
          to="/"
          class="p-2 rounded-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-200 hover:scale-105"
        >
          <IconHome class="w-6 h-6 text-gray-600 dark:text-gray-300" />
        </router-link>
      </div>

      <!-- Menú móvil -->
      <div class="md:hidden">
        <button
          @click="toggleMobileMenu"
          class="p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
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
          href="/faq"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Preguntas frecuentes
        </a>
        <a
          href="/who-are-we"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          ¿Quiénes somos?
        </a>
        <a
          href="/data-protection"
          class="text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          ¿Cómo protegemos los datos?
        </a>

        <router-link
          to="/login"
          class="text-left text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors duration-200"
        >
          Iniciar sesión
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// Importando solo los iconos de Tabler que necesitas
import { IconHome, IconMenu2 } from '@tabler/icons-vue'
import { useThemeStore } from '@/store/theme'

const theme = useThemeStore()
const showMobileMenu = ref(false)
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}
</script>
