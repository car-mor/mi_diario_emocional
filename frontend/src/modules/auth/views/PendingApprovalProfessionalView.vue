<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4 transition-colors">
    <div class="max-w-md w-full text-center bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">

      <!-- Icono y Título -->
      <div class="flex flex-col items-center mb-6">
        <IconClockHour4 class="w-20 h-20 text-yellow-500 mb-4" />
        <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
          Cuenta Pendiente de Aprobación
        </h1>
      </div>

      <!-- Mensaje Explicativo -->
      <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
        ¡Gracias por verificar tu correo! Tu solicitud de registro está siendo revisada por nuestro equipo de administración para validar tu cédula profesional.
        <br/><br/>
        Te notificaremos por correo electrónico tan pronto como tu cuenta sea aprobada.
      </p>

      <!-- Botón de Salida -->
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
import { IconClockHour4 } from '@tabler/icons-vue';

// Obtenemos la instancia de la tienda de Pinia
const authStore = useAuthStore();

// Función para cerrar la sesión del usuario
const logout = () => {
  authStore.logout();
};
</script>
