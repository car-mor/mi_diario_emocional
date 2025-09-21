<template>
  <div class="p-4 bg-gray-100 dark:bg-gray-900 min-h-screen">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="entry in diaryEntries" :key="entry.id" 
           class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-2xl transition-shadow duration-300">
        
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {{ entry.title }}
        </h2>
        
        <p class="text-gray-700 dark:text-gray-300 italic mb-4">
          "{{ entry.content }}"
        </p>
        
        <p class="text-sm text-gray-500 dark:text-gray-400 text-right">
          {{ entry.date }}
        </p>
      </div>

      <div v-if="diaryEntries.length === 0" class="col-span-1 md:col-span-2 text-center py-10">
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Aún no hay registros en tu diario.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
/* Se usa la importación de onMounted y axios para la conexión con el backend.
  import { onMounted } from 'vue';
  import axios from 'axios';
*/

// Datos de prueba: un array de objetos que simulan registros de diario.
// Cada objeto tiene un id, title, content, y date.
const diaryEntries = ref([
  {
    id: 1,
    title: "Sin título",
    content: "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "3 de Agosto 2022 23:11"
  },
  {
    id: 2,
    title: "Neque porro quisquam est qui dolorem ipsum quia",
    content: "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "3 de Agosto 2022 03:12"
  },
  {
    id: 3,
    title: "Neque porro quisquam est qui dolorem ipsum quia",
    content: "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "3 de Agosto 2022 14:00"
  },
  {
    id: 4,
    title: "Sin título",
    content: "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "3 de Agosto 2022 12:36"
  }
  ,
  {
    id: 5,
    title: "Sin título",
    content: "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "6 de Agosto 2022 12:36"
  }
]);

/* Lógica para consumir datos del backend.
  Se descomenta cuando la API esté lista.
  onMounted(async () => {
    try {
      const response = await axios.get('/api/diary-entries');
      diaryEntries.value = response.data;
    } catch (error) {
      console.error("Error al cargar los registros del diario:", error);
    }
  });
*/

</script>