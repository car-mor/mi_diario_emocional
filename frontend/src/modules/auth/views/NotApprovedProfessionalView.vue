<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4 transition-colors">
    <div class="max-w-md w-full text-center bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">

      <div class="flex flex-col items-center mb-6">
        <IconCircleXFilled class="w-20 h-20 text-red-500 mb-4" />
        <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
          Solicitud de Registro No Aprobada
        </h1>
      </div>

      <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
        Lamentamos informarte que, tras revisar tu solicitud, tu cuenta de profesional no ha sido aprobada.
        <br/><br/>
        Esto suele deberse a inconsistencias en los datos proporcionados o en la validación de la cédula profesional.
        <br/><br/>
        Si crees que esto es un error, por favor, ponte en contacto con nuestro equipo de soporte: <strong>midiarioemocional_help@outlook.com</strong>
      </p>

      <button
        @click="logout"
        class="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Cerrar Sesión
      </button>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth';
// Importamos el nuevo ícono
import { IconCircleXFilled } from '@tabler/icons-vue';

// Obtenemos la instancia de la tienda de Pinia
const authStore = useAuthStore();

// La función de logout sigue siendo la misma
const logout = () => {
  authStore.logout();
};
</script>
