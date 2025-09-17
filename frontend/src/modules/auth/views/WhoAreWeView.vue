<template>
  <div
    class="py-10 lg:py-20 px-4 md:px-8 bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center mb-16">
      <div class="text-center lg:text-left">
        <h2 class="text-4xl md:text-5xl font-bold mb-4 text-[#70BFE9]">¿Quiénes somos?</h2>
        <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
          En Diario Emocional, creemos en el poder de la tecnología para transformar nuestro
          bienestar. Nuestro proyecto nació de la necesidad de entender mejor nuestras emociones en
          el mundo digital. Somos un equipo apasionado que combina la inteligencia artificial con la
          psicología para crear herramientas que te ayuden a reflexionar, crecer y gestionar tu
          salud emocional.
        </p>
        <button
          class="inline-block bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-8 rounded-full shadow-lg transition-colors"
        >
          Saber más
        </button>
      </div>

      <div class="flex justify-center lg:justify-end">
        <img
          src="@/assets/images/cerebro_feliz.png"
          alt="Ilustración del equipo"
          class="rounded-lg w-64 h-64 md:w-80 md:h-80 lg:w-auto lg:h-[400px] dark:border-gray-700"
        />
      </div>
    </div>

    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
      <!-- Misión -->
      <div
        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 h-full flex flex-col items-center justify-start transition-colors"
      >
        <h3 class="text-2xl font-bold mb-6 text-[#70BFE9] dark:text-[#70BFE9]">Misión</h3>
        <p class="text-base text-gray-600 dark:text-gray-300 text-justify space-y-4">
          Desarrollar y proporcionar una herramienta tecnológica innovadora basada en el
          Procesamiento de Lenguaje Natural (NLP) que permita la identificación y clasificación de
          emociones combinadas en textos en español, mediante un diario emocional digital accesible
          a través de una aplicación web.
        </p>
        <p class="text-base text-gray-600 dark:text-gray-300 text-justify space-y-4 pt-4">
          Nuestro propósito es apoyar a profesionales de la salud mental y a sus pacientes en el
          proceso terapéutico, promoviendo la conciencia emocional y la escritura expresiva, con el
          fin de mejorar el bienestar psicológico en el contexto hispanohablante.
        </p>
      </div>

      <!-- Visión -->
      <div
        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 h-full flex flex-col items-center justify-start transition-colors"
      >
        <h3 class="text-2xl font-bold mb-6 text-[#70BFE9] dark:text-[#70BFE9]">Visión</h3>
        <p class="text-base text-gray-600 dark:text-gray-300 text-justify space-y-4">
          Convertirnos en una referencia líder en la integración de tecnología y salud mental,
          ofreciendo una solución pionera que supere las limitaciones de las herramientas actuales
          de análisis emocional.
        </p>
        <p class="text-base text-gray-600 dark:text-gray-300 text-justify space-y-4 pt-4">
          Aspiramos a que nuestro prototipo evolucione en una plataforma ampliamente adoptada por
          profesionales de la salud mental y pacientes, reconocida por su capacidad para detectar
          emociones combinadas en español con precisión y por su contribución al fortalecimiento de
          procesos terapéuticos.
        </p>
        <p class="text-base text-gray-600 dark:text-gray-300 text-justify space-y-4 pt-4">
          Buscamos impactar positivamente la calidad de vida de las personas y fomentar un enfoque
          más adaptativo hacia la gestión emocional en la sociedad moderna.
        </p>
      </div>

      <!-- Servicios -->
      <div
        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 h-full flex flex-col items-center justify-start transition-colors"
      >
        <h3 class="text-2xl font-bold mb-6 text-[#70BFE9] dark:text-[#70BFE9]">Servicios</h3>
        <ul class="list-disc list-inside text-left space-y-4 text-gray-600 dark:text-gray-300">
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white">Análisis de Datos:</span>
            Recopilamos, filtramos y preprocesamos textos en español provenientes de distintas
            fuentes, con el objetivo de identificar patrones y emociones combinadas, asegurando la
            calidad y coherencia de la información para entrenar modelos precisos de NLP.
          </li>
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white"
              >Desarrollo de Modelos de IA:</span
            >
            Implementamos y entrenamos modelos de inteligencia artificial capaces de reconocer y
            clasificar emociones complejas en textos, combinando técnicas de aprendizaje automático
            y procesamiento de lenguaje natural para ofrecer resultados confiables y adaptados al
            idioma español.
          </li>
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white"
              >Prototipo de Aplicación Web:</span
            >
            Diseñamos e implementamos una aplicación web interactiva que funciona como diario
            emocional digital, permitiendo a los usuarios registrar sus emociones, reflexionar sobre
            ellas y acceder a reportes y análisis visuales que apoyen el trabajo terapéutico con
            profesionales de la salud mental.
          </li>
        </ul>
      </div>
    </div>
  </div>
  <WelcomeFooter />
</template>

<script setup lang="ts">
import WelcomeFooter from '../components/WelcomeFooter.vue'
// No se necesita lógica JS para este componente estático
</script>
