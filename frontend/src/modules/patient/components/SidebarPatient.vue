<template>
  <div>
    <button
      @click="toggleMobileMenu"
      class="md:hidden fixed top-4 left-4 z-50 p-2 rounded-full bg-[#7DBFF8] text-white shadow-lg active:scale-95 transition-transform"
    >
      <IconMenu2 class="w-6 h-6" />
    </button>

    <div
      v-if="showMobileMenu"
      @click="showMobileMenu = false"
      class="fixed inset-0 z-30 md:hidden"
    ></div>

    <aside
      :class="[
        'dark:bg-gray-900 transition-colors fixed md:static top-0 left-0 h-full bg-[#7DBFF8] text-white flex flex-col items-center py-6 shadow-xl z-40',
        showMobileMenu ? 'translate-x-0 w-64' : '-translate-x-full w-18',
        'md:translate-x-0 md:w-20 lg:w-24 md:overflow-visible overflow-y-auto transition-all duration-300'
      ]"
    >
      <nav class="flex flex-col space-y-4 md:space-y-6 flex-1 mt-12 md:mt-6 w-full px-2">

        <router-link
          v-for="(item, index) in menuItems"
          :key="index"
          :to="item.path"
          :class="[
            'group relative flex items-center p-3 rounded-xl transition-all duration-300',
            showMobileMenu ? 'justify-start px-4' : 'justify-center',
            'hover:bg-[#5aa7d1] dark:hover:bg-gray-700'
          ]"
          @click="showMobileMenu = false"
        >
          <component
            :is="item.icon"
            :class="[
               'w-8 h-8 md:w-9 md:h-9 flex-shrink-0 transition-transform group-hover:scale-110',
               item.mobileOnly ? 'md:hidden' : ''
            ]"
          />

          <span
            v-if="showMobileMenu"
            class="ml-4 font-medium text-lg md:hidden whitespace-nowrap"
          >
            {{ item.name }}
          </span>

          <div
            class="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2
                   bg-gray-800 text-white text-sm rounded-md shadow-lg
                   opacity-0 invisible -translate-x-2
                   group-hover:opacity-100 group-hover:visible group-hover:translate-x-0
                   transition-all duration-200 z-50 whitespace-nowrap pointer-events-none hidden md:block"
          >
            {{ item.name }}
            <div class="absolute top-1/2 right-full -translate-y-1/2 -mr-1 border-4 border-transparent border-r-gray-800"></div>
          </div>
        </router-link>

      </nav>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from "vue"
import {
  IconHome, IconMenu2, IconBook, IconClock, IconChartPie2,
  IconCloud, IconHelpHexagon, IconSettings, IconUserCircle
} from "@tabler/icons-vue"

const showMobileMenu = ref(false)
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const menuItems = [
  // He añadido la propiedad 'mobileOnly' para el perfil, por si quieres ocultar el icono en desktop también
  { name: 'Mi Perfil', path: '/profile-patient-mobile', icon: markRaw(IconUserCircle), mobileOnly: true },
  { name: 'Inicio', path: '/home-patient', icon: markRaw(IconHome) },
  { name: 'Diario', path: '/diary-register', icon: markRaw(IconBook) },
  { name: 'Historial', path: '/diary-history', icon: markRaw(IconClock) },
  { name: 'Estadísticas', path: '/pie-chart-patient', icon: markRaw(IconChartPie2) },
  { name: 'Nube Emocional', path: '/word-cloud-patient', icon: markRaw(IconCloud) },
  { name: 'Preguntas', path: '/faqs-patient', icon: markRaw(IconHelpHexagon) },
  { name: 'Configuración', path: '/account-settings', icon: markRaw(IconSettings) },
]
</script>
