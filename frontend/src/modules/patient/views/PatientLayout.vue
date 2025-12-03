<template>
    <div class="flex h-screen">
        <!-- Sidebar izquierdo component -->

        <Sidebar />
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <!-- header con título y racha component-->
            <StreakAndTitle
              title=""
              :streak-count="streakCount"
            />
        </main>
        <!-- Perfil del usuario(solo en pantallas grandes) component -->
        <UserProfile />
    </div>
    <div v-if="showWarningModal" class="fixed inset-0 z-[100] flex items-center justify-center" aria-modal="true">
    <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl max-w-md w-full text-center mx-4">

      <svg class="w-16 h-16 text-yellow-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>

      <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">¿Sigues ahí?</h2>
      <p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
        Tu sesión se cerrará por inactividad en <b>2 minutos</b>.
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
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useAuthStore } from '@/store/auth';
import Sidebar from "../components/SidebarPatient.vue"

const countdown = ref(120); // 2 minutos en segundos

const authStore = useAuthStore(); // Ya deberías tener esto

// Variable para mostrar el modal de advertencia
const showWarningModal = ref(false);

// Tiempos (en milisegundos)
const WARNING_TIME_MS = 10 * 60 * 1000; // 10 minutos
const COUNTDOWN_SECONDS = 120; // 2 minutos

// IDs de los temporizadores (para poder limpiarlos)
let warningTimerId: number | null = null;
let logoutTimerId: number | null = null; // ← Cambiar de const a let
let countdownInterval: number | null = null;

/**
 * Inicia los dos temporizadores: uno para la advertencia (9 min)
 * y otro para el cierre de sesión automático (10 min).
 */
const startInactivityTimers = () => {
  if (warningTimerId) clearTimeout(warningTimerId);
  if (logoutTimerId) clearTimeout(logoutTimerId);
  if (countdownInterval) clearInterval(countdownInterval);

  // Timer para mostrar advertencia
  warningTimerId = setTimeout(() => {
    showWarningModal.value = true;
    startCountdown();
  }, WARNING_TIME_MS);

  // Timer para logout automático (advertencia + countdown)
  logoutTimerId = setTimeout(() => {
    authStore.logout();
  }, WARNING_TIME_MS + (COUNTDOWN_SECONDS * 1000));
};

const startCountdown = () => {
  countdown.value = COUNTDOWN_SECONDS;

  // Limpia intervalos anteriores
  if (countdownInterval) clearInterval(countdownInterval);

  countdownInterval = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--;
    } else {
      clearInterval(countdownInterval!);
      authStore.logout(); // Cierra sesión al llegar a 0
    }
  }, 1000);
};

/**
 * Se llama cuando el usuario interactúa con la página (clic, teclado, etc.)
 * o cuando hace clic en "Permanecer Conectado".
 */
const resetInactivityTimer = () => {
  showWarningModal.value = false;
  if (countdownInterval) clearInterval(countdownInterval);
  if (logoutTimerId) clearTimeout(logoutTimerId);
  startInactivityTimers();
};

/**
 * Cierra la sesión manualmente desde el modal.
 */
const manualLogout = () => {
  showWarningModal.value = false;
  if (countdownInterval) clearInterval(countdownInterval);
  if (logoutTimerId) clearTimeout(logoutTimerId); // ← Agregar esta línea
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

interface PatientProfile {
    name: string;
    paternal_last_name: string;
    maternal_last_name: string;
    email: string;
    alias: string;
    gender: string;
    professional_name?: string; // Es opcional y puede ser nulo
    is_linked: boolean;
    current_streak: number;
}

const streakCount = computed(() => {
  // Primero, verificamos si el usuario es un paciente y si su perfil ha cargado
  if (authStore.userType === 'patient' && authStore.userProfile) {
    // Si es así, le decimos a TypeScript que trate el perfil como un PatientProfile
    // y accedemos a 'current_streak' de forma segura.
    return (authStore.userProfile as PatientProfile).current_streak || 0;
  }
  // Si no es un paciente, la racha es 0.
  return 0;
});

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
  if (countdownInterval) clearInterval(countdownInterval);

  activityEvents.forEach(event => {
    window.removeEventListener(event, resetInactivityTimer);
  });
});
</script>
