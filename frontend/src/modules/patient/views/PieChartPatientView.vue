<template>
    <div class="flex h-screen">

        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <StreakAndTitle class="text-center"
              title="Gráfica de pastel de mis emociones"
              :streak-count="streakCount"
            />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Mi análisis de emociones de esta semana
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En esta sección podrás ver una gráfica de tu análisis de emociones hasta ahora, se muestran las 5 combinaciones de emociones más frecuentes que has experimentado basándote en tus entradas del diario de esta semana.
                    </p>
                </div>
                <!-- Contenido principal - component gráfico de pastel -->
                <PieChartPatient
                  :combination-data="emotionCombinations"
                  :loading="loading"
                  :error="error"
                />
                <router-view />
            </div>
        </main>
        <!-- Perfil del usuario component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
    import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
    import UserProfile from "../components/PatientProfile.vue"
    import PieChartPatient from "../components/PieChartPatient.vue"
    import { computed, ref, onMounted } from 'vue';
  import { useAuthStore } from '@/store/auth';
  import * as DiaryService from '@/modules/diary/services/diaryServices';
    const authStore = useAuthStore();

const emotionCombinations = ref<[string, number][]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

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
const getWeekDateRange = (): { start_date: string, end_date: string } => {
  const now = new Date();
  const dayOfWeek = now.getDay(); // 0 (Domingo) - 6 (Sábado)

  // 1. Calcular la diferencia para llegar al Lunes
  // Si es Domingo (0), restamos 6 días. Si es otro día, restamos (dia - 1)
  const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);

  const startOfWeek = new Date(now);
  startOfWeek.setDate(diff);
  startOfWeek.setHours(0, 0, 0, 0); // Forzamos a que sea las 00:00h

  const endOfWeek = new Date(startOfWeek);
  endOfWeek.setDate(startOfWeek.getDate() + 6);
  endOfWeek.setHours(23, 59, 59, 999); // Forzamos fin del día

  // 2. CORRECCIÓN IMPORTANTE: Formatear a YYYY-MM-DD usando hora LOCAL
  const toLocalDateString = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Meses van de 0-11
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  return {
    start_date: toLocalDateString(startOfWeek),
    end_date: toLocalDateString(endOfWeek),
  };
};

onMounted(async () => {
  loading.value = true;
  error.value = null;
  try {
    // Llamamos al servicio de combinaciones de emociones
    const dateFilter = getWeekDateRange(); // 1. Obtiene la semana actual
    // 2. Pasa el filtro a la API
    const response = await DiaryService.getEmotionCombinations(dateFilter);
    emotionCombinations.value = response.data;
  } catch (err) {
    console.error('Fallo al obtener datos para la gráfica:', err);
    error.value = "No se pudieron cargar los datos del análisis.";
  } finally {
    loading.value = false;
  }
});
</script>
