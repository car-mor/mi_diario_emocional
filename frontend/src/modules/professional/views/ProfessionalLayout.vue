<template>
      <div class="dark:bg-gray-900 flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">


    <main class="flex-1 flex flex-col overflow-hidden">
          <header>
      <ProfessionalHeader />
    </header>


      <div class="flex-1 p-6 overflow-y-auto">
        <router-view />
      </div>
    </main>
    <footer>
        <WelcomeFooter />
    </footer>
  </div>
  <div v-if="showWarningModal" class="fixed inset-0 z-[100] flex items-center justify-center" aria-modal="true">
    <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl max-w-md w-full text-center mx-4">

      <svg class="w-16 h-16 text-yellow-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>

      <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">¿Sigues ahí?</h2>
      <p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
        Tu sesión se cerrará por inactividad en <b>1 minuto</b>.
      </p>

      <div class="flex justify-center gap-4">
        <button
          @click="manualLogout"
          class="bg-gray-300 hover:bg-gray-400 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-gray-200 font-semibold py-2 px-6 rounded-lg transition-colors">
          Cerrar Sesión
        </button>
        <button
          @click="resetInactivityTimer"
          class="bg-[#70BFE9] hover:bg-[#5a9cbf] text-white font-semibold py-2 px-6 rounded-lg transition-colors">
          Permanecer Conectado
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 4. Imports necesarios para todos los componentes
import WelcomeFooter from '@/modules/auth/components/WelcomeFooter.vue';
import ProfessionalHeader from '../components/ProfessionalHeader.vue';
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore(); // Ya deberías tener esto

// Variable para mostrar el modal de advertencia
const showWarningModal = ref(false);

// Tiempos (en milisegundos)
const WARNING_TIME_MS = 10 * 60 * 1000; // 10 minutos
const LOGOUT_TIME_MS = 2 * 60 * 1000; // 2 minutos

// IDs de los temporizadores (para poder limpiarlos)
let warningTimerId: number | null = null;
let logoutTimerId: number | null = null;

/**
 * Inicia los dos temporizadores: uno para la advertencia (9 min)
 * y otro para el cierre de sesión automático (10 min).
 */
const startInactivityTimers = () => {
  // 1. Limpia cualquier timer anterior para evitar duplicados
  if (warningTimerId) clearTimeout(warningTimerId);
  if (logoutTimerId) clearTimeout(logoutTimerId);

  // 2. Inicia el timer para la advertencia
  warningTimerId = setTimeout(() => {
    showWarningModal.value = true;
  }, WARNING_TIME_MS);

  // 3. Inicia el timer para el logout automático
  logoutTimerId = setTimeout(() => {
    // Solo cerramos sesión si el modal está activo (por si acaso)
    if (showWarningModal.value) {
      authStore.logout();
    }
  }, LOGOUT_TIME_MS);
};

/**
 * Se llama cuando el usuario interactúa con la página (clic, teclado, etc.)
 * o cuando hace clic en "Permanecer Conectado".
 */
const resetInactivityTimer = () => {
  showWarningModal.value = false; // Oculta el modal
  startInactivityTimers(); // Reinicia el conteo de 10 minutos
};

/**
 * Cierra la sesión manualmente desde el modal.
 */
const manualLogout = () => {
  showWarningModal.value = false;
  authStore.logout();
};

// Lista de eventos que cuentan como "actividad"
const activityEvents: (keyof WindowEventMap)[] = [
  'click',
  'mousemove',
  'keypress',
  'scroll',
  'touchstart'
];

// ----------------------------------------------------
// CICLOS DE VIDA (onMounted / onUnmounted)
// ----------------------------------------------------

onMounted(() => {
  // --- Inicia los timers y los listeners de actividad ---
  startInactivityTimers();
  activityEvents.forEach(event => {
    window.addEventListener(event, resetInactivityTimer);
  });
});

onUnmounted(() => {
  // --- Limpia todo al salir del componente ---
  if (warningTimerId) clearTimeout(warningTimerId);
  if (logoutTimerId) clearTimeout(logoutTimerId);

  activityEvents.forEach(event => {
    window.removeEventListener(event, resetInactivityTimer);
  });
});
</script>
