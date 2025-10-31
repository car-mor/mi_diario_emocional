<template>
    <div class="flex h-screen">
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <StreakAndTitle
              title="Preguntas Frecuentes (FAQs)"
              :streak-count="streakCount"
            />
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Preguntas frecuentes
                    </h2>
                </div>
                <!-- Contenido principal - preguntas -->
                <div class="max-w-3xl mx-auto px-4 dark:bg-gray-900 pt-4 pb-4 rounded-lg">
                    <div class="space-y-4">
                        <div
                        v-for="(item, index) in faqItems"
                        :key="index"
                        class="bg-white rounded-lg shadow-md overflow-hidden dark:text-white dark:bg-gray-800"
                        >
                            <button
                            @click="toggle(index)"
                            class="w-full flex justify-between items-center p-4 text-left font-semibold text-lg text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                            >
                                <span>{{ item.question }}</span>
                                <span>{{ openIndex === index ? '-' : '+' }}</span>
                            </button>

                            <div
                            v-if="openIndex === index"
                            class="p-4 bg-gray-50 border-t border-gray-200 text-gray-700 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 transition-opacity"
                            >
                                <p>{{ item.answer }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="text-center lg:text-left p-5">
                    <h2 class="text-2xl md:text-2xl font-bold mb-4 text-gray-600 dark:text-gray-300 mb-6">
                        ¿Necesitas más información? ¡Contáctanos!
                    </h2>
                    <a
                    href="mailto:midiarioemocional@gmail.com"
                    class="text-lg md:text-4xl text-[#70BFE9] font-bold"
                    >
                        <IconMailHeart class="inline w-11 h-11 md:w-11 md:h-11 mr-2 mb-1" />
                        midiarioemocional@gmail.com
                    </a>

                </div>

                <router-view />
            </div>
        </main>
        <!-- Perfil del usuario(solo en pantallas grandes) component -->
        <UserProfile />
    </div>
</template>

<script setup lang="ts">
import { IconMailHeart } from "@tabler/icons-vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import UserProfile from "../components/PatientProfile.vue"
import { ref } from 'vue';

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

const openIndex = ref<number | null>(null)

const faqItems = [
  {
    question: '¿Qué hago si olvidé mi contraseña o no puedo iniciar sesión?',
    answer: 'Puedes utilizar la opción de "Olvidé mi contraseña" en la página de inicio de sesión para restablecer tu contraseña mediante tu correo electrónico. En caso de presentar problemas, contacta con nuestro equipo de soporte.',
  },
  {
    question: '¿Puedo cambiar mi alias, foto de perfil o correo electrónico?',
    answer:
      'Sí, puedes actualizar tu información personal en la sección de configuración de tu cuenta.',
  },
  {
    question: '¿Cómo puedo contactar al equipo?',
    answer:
      'Puedes encontrarnos a través de la información de contacto en la parte inferior de la página.',
  },
  {
    question: '¿Quién puede ver mis emociones y mis notas?',
    answer:
      'Únicamente tu especialista de la salud mental y tú.',
  },
  {
    question: '¿Puedo usar la página sin conexión a internet?',
    answer:
      'No, la página requiere una conexión a internet para funcionar correctamente.',
  },
  {
    question: '¿Qué significan los resultados de las emociones combinadas?',
    answer:
      'Los resultados de las emociones combinadas reflejan la interacción entre diferentes emociones y pueden proporcionar una visión más completa de tu estado emocional.',
  },
]

const toggle = (index: number) => {
  if (openIndex.value === index) {
    openIndex.value = null
  } else {
    openIndex.value = index
  }
}

</script>
