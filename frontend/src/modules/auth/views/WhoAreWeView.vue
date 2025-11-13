<template>
  <div
    class="py-10 lg:py-20 px-4 md:px-8 bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center mb-16">
      <div class="text-center">
        <h2 class="text-4xl lg:text-left md:text-5xl font-bold mb-4 text-[#70BFE9]">¿Quiénes somos?</h2>
        <br>
        <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6 text-justify">
          En "Mi diario emocional" vemos la tecnología como una aliada para tu bienestar. <br><br>

Este proyecto nació para crear un espacio seguro donde puedas entender mejor cómo te sientes. Combinamos los avances de la inteligencia artificial con principios de psicología para ofrecerte una herramienta que te ayude a reflexionar, crecer y tomar el control de tu bienestar emocional cada día.
        </p>

        <router-link
              to="/login"
              class="inline-block bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-8 rounded-full shadow-lg transition-colors"
            >
              Crear cuenta
            </router-link>
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
        <p class="text-xl text-gray-600 dark:text-gray-300 text-justify space-y-4 pt-4">
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
        <p class="text-xl text-gray-600 dark:text-gray-300 text-justify space-y-4 pt-4">
          Aspiramos a que nuestro prototipo evolucione en una plataforma ampliamente adoptada por
          profesionales de la salud mental y pacientes, reconocida por su capacidad para detectar
          emociones combinadas en español con precisión y por su contribución al fortalecimiento de
          procesos terapéuticos.
        </p>
      </div>

      <!-- Servicios -->
      <div
        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 h-full flex flex-col items-center justify-start transition-colors"
      >
        <h3 class="text-2xl font-bold mb-6 text-[#70BFE9] dark:text-[#70BFE9]">Servicios</h3>
        <ul class="list-disc list-inside text-xl text-left space-y-4 text-gray-600 dark:text-gray-300">
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white">Diario emocional digital:</span> <br>
            Un espacio privado y seguro para registrar tus pensamientos, reflexionar sobre tu día y liberar tus emociones.
          </li>
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white"
              >Recursos de autoayuda:</span
            ><br>
           Accede a una biblioteca de artículos, videos, audiolibros y técnicas de relajación diseñadas por expertos para ayudarte a gestionar tus emociones en el momento.
          </li>
          <li class="text-justify">
            <span class="font-semibold text-gray-900 dark:text-white"
              >Seguimiento emocional:</span
            ><br>
            Visualiza cómo evolucionan tus emociones a lo largo del tiempo.
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
