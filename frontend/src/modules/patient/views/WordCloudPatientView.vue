<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Nube de Palabras</h1>

    <p class="mb-4 text-gray-600">
      Esta visualización muestra las emociones más mencionadas por el paciente.
    </p>

    <!-- Aquí ya usas el componente -->
    <WordCloudChart  />
  </div>
</template>

<script setup lang="ts">
import WordCloudChart from "../components/WordCloudPatient.vue";

</script>
