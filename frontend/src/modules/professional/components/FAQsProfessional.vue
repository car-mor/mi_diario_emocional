<template>
    <div class="flex">
        <!-- Área principal central -->
        <main class="flex-1 flex flex-col overflow-hidden">
            <div class="dark:bg-gray-800 transition-colors flex-1 p-4 overflow-y-auto">
                <div class="p-4 flex flex-col text-left">
                    <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                        Soporte al cliente y Preguntas frecuentes
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
    </div>
</template>

<script setup lang="ts">
import { IconMailHeart, IconBackspaceFilled } from "@tabler/icons-vue"
import { ref } from 'vue';

const openIndex = ref<number | null>(null)
const faqItems = [
  {
    question: '¿Qué hago si olvidé mi contraseña o no puedo iniciar sesión?',
    answer: 'Puedes utilizar la opción de "Olvidé mi contraseña" en la página de inicio de sesión para restablecer tu contraseña mediante tu correo electrónico. En caso de presentar problemas, contacta con nuestro equipo de soporte.',
  },
  {
    question: '¿Qué información puedo actualizar en mi perfil?',
    answer:
      'Puedes actualizar tu correo electrónico, y contraseña. Si necesitas más información, por favor contacta con nuestro equipo de soporte.',
  },
  {
    question: '¿Cómo puedo contactar al equipo?',
    answer:
      'Puedes encontrarnos a través de la información de contacto en la parte inferior de la página.',
  },
  {
    question: '¿Cómo veo el resumen de mis pacientes?',
    answer:
      'Puedes acceder al resumen de tus pacientes desde el panel de control en la sección "Gestionar pacientes".',
  },
  {
    question: '¿Puedo usar la página sin conexión a internet?',
    answer:
      'No, la página requiere una conexión a internet para funcionar correctamente.',
  },
  {
    question: '¿Qué significan los resultados de las emociones combinadas?',
    answer:
      'Los resultados de las emociones combinadas reflejan la interacción entre diferentes emociones y pueden proporcionar una visión más completa del estado emocional.',
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
