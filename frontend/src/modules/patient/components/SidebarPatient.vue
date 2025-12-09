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
      @click.stop="showMobileMenu = false"
      class="fixed inset-0 z-30 md:hidden bg-black/0 w-full h-full cursor-pointer"
    ></div>

    <aside
      :class="[
        'dark:bg-gray-900 transition-colors fixed md:static top-0 left-0 h-full bg-[#7DBFF8] text-white flex flex-col items-center py-6 shadow-xl z-40',
        showMobileMenu ? 'translate-x-0 w-64' : '-translate-x-full w-18',
        'md:translate-x-0 md:w-20 lg:w-24 md:overflow-visible overflow-y-auto transition-all duration-300'
      ]"
    >
      <nav class="flex flex-col space-y-4 md:space-y-6 flex-1 w-full px-2 justify-center">

        <component
          v-for="(item, index) in menuItems"
          :key="index"
          :is="item.path ? 'router-link' : 'button'"
          :to="item.path"
          @click="handleItemClick(item)"
          :class="[
            'group relative flex items-center p-3 rounded-xl transition-all duration-300 w-full',
            showMobileMenu ? 'justify-start px-4' : 'justify-center',
            'hover:bg-[#5aa7d1] dark:hover:bg-gray-700 text-white',
            // CAMBIO AQUÍ: Si es mobileOnly, ocultamos TODO el botón en desktop (md:hidden)
            item.mobileOnly ? 'md:hidden' : ''
          ]"
        >
          <component
            :is="item.icon"
            class="w-8 h-8 md:w-9 md:h-9 flex-shrink-0 transition-transform group-hover:scale-110"
          />

          <span
            v-if="showMobileMenu"
            class="ml-4 font-medium text-lg md:hidden whitespace-nowrap"
          >
            {{ item.name }}
          </span>

          <div
            v-if="!item.mobileOnly"
            class="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2
                   bg-gray-800 text-white text-sm rounded-md shadow-lg
                   opacity-0 invisible -translate-x-2
                   group-hover:opacity-100 group-hover:visible group-hover:translate-x-0
                   transition-all duration-200 z-50 whitespace-nowrap pointer-events-none hidden md:block"
          >
            {{ item.name }}
            <div class="absolute top-1/2 right-full -translate-y-1/2 -mr-1 border-4 border-transparent border-r-gray-800"></div>
          </div>
        </component>

      </nav>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from "vue"
import type { Component } from "vue"
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import {
  IconHome, IconMenu2, IconBook, IconClock, IconChartPie2,
  IconCloud, IconHelpHexagon, IconSettings, IconUserCircle,
  IconLogout
} from "@tabler/icons-vue"

interface MenuItem {
  name: string;
  path?: string;
  icon: Component | object;
  mobileOnly?: boolean;
  action?: () => void;
}

const router = useRouter()
const authStore = useAuthStore()
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push({ name: 'login' })
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
    router.push({ name: 'login' })
  }
}

const handleItemClick = (item: MenuItem) => {
  showMobileMenu.value = false

  if (item.action) {
    item.action()
  }
}

const menuItems: MenuItem[] = [
  // Mi Perfil ya estaba como mobileOnly: true
  { name: 'Mi Perfil', path: '/profile-patient-mobile', icon: markRaw(IconUserCircle), mobileOnly: true },
  { name: 'Inicio', path: '/home-patient', icon: markRaw(IconHome) },
  { name: 'Diario', path: '/diary-register', icon: markRaw(IconBook) },
  { name: 'Historial', path: '/diary-history', icon: markRaw(IconClock) },
  { name: 'Estadísticas', path: '/pie-chart-patient', icon: markRaw(IconChartPie2) },
  { name: 'Nube Emocional', path: '/word-cloud-patient', icon: markRaw(IconCloud) },
  { name: 'Preguntas', path: '/faqs-patient', icon: markRaw(IconHelpHexagon) },
  { name: 'Configuración', path: '/account-settings', icon: markRaw(IconSettings) },
  {
    name: 'Cerrar sesión',
    icon: markRaw(IconLogout),
    action: handleLogout,
    mobileOnly: true // <--- CAMBIO: Agregado para que solo salga en móvil
  },
]
</script>
