<template>
    <div class="flex h-screen">
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <StreakAndTitle
              title="Diario: Registra tus emociones"
              :streak-count="streakCount"
            />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Hoy es un buen día para escribir en tu diario
                    </h2>
                </div>
                <!-- Descripción -->
                <div class="text-center lg:text-left p-4">
                    <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
                        En esta sección puedes registrar tus emociones y pensamientos diarios. Recuerda que expresar lo que sientes puede ayudarte a comprenderte mejor y a manejar tus emociones de manera saludable.
                    </p>
                </div>
                <!-- Contenido principal - component  -->
                <DiaryRegister />
                <router-view />
            </div>
        </main>
        <!-- Perfil del usuario component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
   import StreakAndTitle from "../components/StreakAndTitlePatient.vue";
    import UserProfile from "../components/PatientProfile.vue"
    import DiaryRegister from "../components/DiaryRegister.vue"
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
