<template>
    <div class="flex h-screen">

        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
          <StreakAndTitle class="text-center"
              title="Nube de Palabras de mis emociones"
              :streak-count="streakCount"
            />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        ¡Mira, esa nube tiene forma de estrella!
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En la sección de Nube de Palabras, podrás ver una recopilación de las palabras que más has ustilizado hasta ahora ¡Entre más grande la palabra más veces la has usado!
                    </p>
                </div>
                <!-- Contenido principal - component nube de palabras -->
                <WordCloudPatient />
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
    import WordCloudPatient from "../components/WordCloudPatient.vue"
     import { computed } from 'vue';
  import { useAuthStore } from '@/store/auth';
    const authStore = useAuthStore();

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
</script>
