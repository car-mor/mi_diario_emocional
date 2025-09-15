<template>
  <div
    class="grid grid-rows-[auto_1fr_auto] min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <main class="py-10 pb-28">
      <div class="max-w-3xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-8 text-[#70BFE9]">Preguntas frecuentes</h2>

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
    </main>

    <WelcomeFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import WelcomeFooter from '../components/WelcomeFooter.vue'

const openIndex = ref<number | null>(null)

const faqItems = [
  {
    question: '¿Qué es Diario Emocional?',
    answer: 'Es una aplicación para registrar y gestionar tus emociones a lo largo del tiempo.',
  },
  {
    question: '¿Mis datos están seguros?',
    answer:
      'Sí, toda tu información se almacena de forma segura y se rige por la Declaración ISO/IEC 27001.',
  },
  {
    question: '¿Cómo puedo contactar al equipo?',
    answer:
      'Puedes encontrarnos a través de la información de contacto en la parte inferior de la página.',
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
