<template>
  <div class="p-4 bg-gray-100 dark:bg-gray-900 ">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="entry in diaryEntries"
        :key="entry.id"
        @click="openModal(entry)"
        class="cursor-pointer bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-2xl transition-shadow duration-300"
      >
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {{ entry.title }}
        </h2>

        <p class="text-gray-700 dark:text-gray-300 italic mb-4 line-clamp-2">
          "{{ entry.content }}"
        </p>

        <p class="text-sm text-gray-500 dark:text-gray-400 text-right">
          {{ entry.date }}
        </p>
      </div>

      <div
        v-if="diaryEntries.length === 0"
        class="flex flex-col col-span-1 md:col-span-2 text-center py-10 items-center justify-center"
      >
      <IconBellRingingFilled class="w-12 h-12 text-yellow-400 mb-4 items-center justify-center" />
        <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
            ¡Aún hay mucho por escribir!
        </h2>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Aún no hay registros en tu diario.
        </p>
      </div>
    </div>

    <!-- Modal -->
    <div
  v-if="isModalOpen"
  class="fixed inset-0 flex items-center justify-center z-50"
>
  <div
    class="bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6 max-w-lg w-full relative"
  >
    <button
      @click="closeModal"
      class="absolute top-3 right-3 text-gray-500 hover:text-gray-800 dark:hover:text-gray-200"
    >
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <div class="pr-12 pt-4">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        {{ selectedEntry?.title }}
      </h2>

      <p class="text-gray-700 dark:text-gray-300 mb-6 whitespace-pre-line">
        {{ selectedEntry?.content }}
      </p>

      <p class="text-sm text-gray-500 dark:text-gray-400 text-right">
        {{ selectedEntry?.date }}
      </p>
    </div>
  </div>
</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { IconBellRingingFilled } from "@tabler/icons-vue"
/**PARA BACKEND 
 * 
 * 
import { ref, onMounted } from 'vue';
import axios from 'axios';

const diaryEntries = ref<DiaryEntry[]>([]);

onMounted(async () => {
  try {
    const response = await axios.get('/api/diary-entries');
    diaryEntries.value = response.data;
  } catch (error) {
    console.error("Error al cargar los registros del diario:", error);
  }
});
*/


//0 entradas de ejemplo
//const diaryEntries = ref<DiaryEntry[]>([]);

type DiaryEntry = {
  id: number;
  title: string;
  content: string;
  date: string;
};

const diaryEntries = ref<DiaryEntry[]>([
  {
    id: 1,
    title: "Sin título",
    content:
      "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...",
    date: "3 de Agosto 2022 23:11",
  },
  {
    id: 2,
    title: "Neque porro quisquam est qui dolorem ipsum quia",
    content:
      "Texto más largo que solo se verá completo al abrir el modal. Aquí podrías mostrar todo el contenido del diario sin recortes ni estilos de line-clamp.",
    date: "3 de Agosto 2022 03:12",
  },
  {
    id: 3,
    title: "Otro registro",
    content: "Contenido corto.",
    date: "3 de Agosto 2022 14:00",
  },
  {
    id: 4,
    title: "Otro registro",
    content: "Contenido corto.",
    date: "3 de Agosto 2022 14:00",
  },
  {
    id: 5,
    title: "Otro registro",
    content: "Contenido corto.",
    date: "3 de Agosto 2022 14:00",
  },
]);

const isModalOpen = ref(false);
const selectedEntry = ref<DiaryEntry | null>(null);

function openModal(entry: DiaryEntry) {
  selectedEntry.value = entry;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  selectedEntry.value = null;
}
</script>
