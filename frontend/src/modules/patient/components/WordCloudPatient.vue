<template>
  <div class="w-full h-96 bg-white rounded-lg shadow p-4">
    <vue-word-cloud
      :words="words"
      font-family="Quicksand, Arial, sans-serif"
      :color="([, weight]: [string, number]) => weight > 50 ? 'purple' : weight > 20 ? 'orange' : 'green' "
    />
  </div>
</template>

<script setup lang="ts">
import VueWordCloud from "vuewordcloud";

const words: [string, number][] = [
  ["feliz", 50],
  ["triste", 30],
  ["emocionado", 20],
  ["ansioso", 15],
  ["calmado", 10],
  ["motivado", 25],
  ["estresado", 18],
    ["sorprendido", 22],
    ["frustrado", 12],
    ["agradecido", 100],
];
</script>
