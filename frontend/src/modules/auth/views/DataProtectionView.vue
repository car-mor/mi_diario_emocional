<template>
  <div
    class="grid grid-rows-[auto_1fr_auto] min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <main class="py-10 pb-28">
      <div class="max-w-3xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-8 text-[#70BFE9] dark:text-gray-300">
          Protección de datos y seguridad
        </h2>

        <p class="text-center text-lg text-gray-700 dark:text-gray-400 mb-10">
          Debido a la naturaleza sensible del proyecto, hemos adoptado directrices de la norma
          **ISO/IEC 27001** como guía para la confidencialidad y protección de tus datos.
          Consideramos la viabilidad de implementar un SGSI (Sistema de Gestión de Seguridad de la
          Información) en el futuro para garantizar un estándar aún más alto.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 text-center">
            <IconLockSquareRounded class="h-12 w-12 mx-auto text-[#70BFE9] dark:text-gray-300" />
            <h3 class="font-bold text-xl mb-2 text-gray-900 dark:text-white">Confidencialidad</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Solo el personal autorizado tendrá acceso a tu información, garantizando la privacidad
              en cada paso.
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 text-center">
            <IconShieldLock class="h-12 w-12 mx-auto text-[#70BFE9] dark:text-gray-300" />
            <h3 class="font-bold text-xl mb-2 text-gray-900 dark:text-white">
              Protección de datos
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              Toda tu información está protegida de cualquier eliminación, modificación o acceso no
              autorizado.
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 text-center">
            <IconFileTextShield class="h-12 w-12 mx-auto text-[#70BFE9] dark:text-gray-300" />
            <h3 class="font-bold text-xl mb-2 text-gray-900 dark:text-white">Seguridad</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Nuestro compromiso es mantener tus datos seguros y garantizar la integridad de toda la
              información.
            </p>
          </div>
        </div>
      </div>
    </main>

    <WelcomeFooter />
  </div>
</template>

<script setup lang="ts">
import WelcomeFooter from '../components/WelcomeFooter.vue'
import { IconLockSquareRounded, IconShieldLock, IconFileTextShield } from '@tabler/icons-vue'
</script>
