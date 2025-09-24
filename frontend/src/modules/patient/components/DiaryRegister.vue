<template>
  <div class="flex flex-col items-center justify-center p-6 bg-gray-50 dark:bg-gray-900">

    <!-- Paso 1: Seleccionar emociones (opcional) -->
    <div v-if="step === 1" class="w-full max-w-lg">
      <h2 class="text-xl font-semibold mb-4 dark:text-white">Paso 1: Antes de escribir</h2>
      <p class="mb-4 dark:text-white">¿Cómo te sientes en este momento?</p>
      <div class="flex justify-around mb-6">
        <label v-for="emo in emotions" :key="emo.value" class="flex flex-col items-center">
          <input type="checkbox" v-model="selectedEmotions" :value="emo.value" />
          <span class="dark:text-white text-3xl">{{ emo.label }}</span>
        </label>
      </div>
      <button class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold" @click="step++">Siguiente</button>
    </div>

    <!-- Paso 2: Escribir contenido del diario (obligatorio) -->
    <div v-if="step === 2" class="w-full max-w-lg">
      <h2 class="text-xl font-semibold mb-4 dark:text-white">Paso 2: ¿Qué tal si escribimos un rato?</h2>
      <textarea
        color="dark:white"
        v-model="content"
        class="w-full h-40 p-3 border rounded dark:text-white"
        placeholder="Hoy me siento..."
      ></textarea>
      <p v-if="contentError" class="text-red-500 text-sm mt-1">{{ contentError }}</p>
      <div class="flex justify-between mt-4">
        <button class="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded" @click="step--">Atrás</button>
        <button class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold" @click="validateContent">Siguiente</button>
      </div>
    </div>

    <!-- Paso 3: Agregar título (obligatorio) -->
    <div v-if="step === 3" class="w-full max-w-lg">
      <h2 class="text-xl dark:text-white font-semibold mb-4">Paso 3: Hora de agregar un título</h2>
      <input
        v-model="title"
        class="w-full p-3 border rounded mb-4 dark:text-white"
        placeholder="Sin título..."
      />
      <p v-if="titleError" class="text-red-500 text-sm mt-1">{{ titleError }}</p>
      <div class="flex justify-between">
        <button class="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded" @click="step--">Atrás</button>
        <button class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold" @click="showConfirmation">Guardar</button>
      </div>
    </div>

    <!-- Modal Confirmación antes de guardar -->
    <div v-if="showConfirmationModal" class="fixed inset-0 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
        <p class="text-lg font-semibold mb-4 dark:text-white">¿Estás seguro(a) de registrar esta entrada a tu diario de emociones?</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">Nota: no podrás modificar nuevamente este texto.</p>
        <div class="flex justify-around space-x-4">
          <button @click="saveEntry" class="px-4 py-2 bg-[#7DBFF8] hover:bg-[#3457B2] text-white rounded font-semibold w-full">Sí</button>
          <button @click="cancelSave" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded font-semibold w-full">No</button>
        </div>
      </div>
    </div>

    <!-- Modal Éxito al guardar -->
    <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-xl max-w-sm w-full text-center">
        <div class="flex justify-center mb-4">
          <div class="bg-green-500 p-2 rounded-full inline-flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <h3 class="text-xl font-bold mb-2 dark:text-white">Entrada guardada</h3>
        <p class="text-gray-600 mb-6 dark:text-gray-400">¡Tu entrada al diario de emociones ha sido registrada con éxito!</p>
        <button @click="closeSuccessModal" class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg w-full">Entendido</button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const step = ref(1);
//emociones basicas de ekman
const emotions = [
  { value: "alegría", label: "😊" },
  { value: "tristeza", label: "😢" },
  { value: "ira", label: "😡" },
  { value: "miedo", label: "😨" },
  { value: "asco", label: "🤢" },
  { value: "sorpresa", label: "😯" },
];
const selectedEmotions = ref<string[]>([]);
const content = ref("");
const title = ref("");
const contentError = ref<string | null>(null);
const titleError = ref<string | null>(null);
//  Variable para controlar la visibilidad del modal
const showConfirmationModal = ref(false);
// Variable para controlar el modal de éxito
const showSuccessModal = ref(false);

function validateContent() {
  const cleanContent = content.value.trim();
  if (cleanContent.length < 100) {
    contentError.value = "Tu diario debe tener al menos 100 caracteres.";
    return;
  }
  if (cleanContent.length > 16000) {
    contentError.value = "Tu diario no puede exceder los 16,000 caracteres.";
    return;
  }
  contentError.value = null;
  step.value++;
}

// Nuevo: Función que valida y luego muestra el modal
function showConfirmation() {
  const cleanTitle = title.value.trim();

  if (cleanTitle.length > 0) {
    if (cleanTitle.length < 3) {
      titleError.value = "El título debe tener al menos 3 caracteres.";
      return;
    }
    if (cleanTitle.length > 100) {
      titleError.value = "El título no puede exceder los 100 caracteres.";
      return;
    }
    const validCharacters = /^[a-zA-Z0-9\s.,!¡¿?_'-]*$/;
    if (!validCharacters.test(cleanTitle)) {
      titleError.value = "El título contiene caracteres no válidos.";
      return;
    }
  } else {
    titleError.value = "Tu diario debe tener un título.";
    return;
  }

   // Si todas las validaciones pasan, muestra el modal de confirmación
  titleError.value = null;
  showConfirmationModal.value = true;
}

// Nuevo: Función para cancelar el guardado
function cancelSave() {
  showConfirmationModal.value = false;
}

// Nuevo: Función para cerrar el modal de éxito y resetear el formulario
function closeSuccessModal() {
  showSuccessModal.value = false;
  step.value = 1;
  selectedEmotions.value = [];
  content.value = "";
  title.value = "";
}

// SIMULACIOOOOOOOOOOOON DE DATOOOS
async function saveEntry() {
  showConfirmationModal.value = false; // Cierra el modal antes de guardar
  
  const payload = {
    emotions: selectedEmotions.value,
    content: content.value.trim(),
    title: title.value.trim(),
    date: new Date().toISOString(),
  };

  try {
     // Simulación de respuesta del servidor
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("Datos enviados (mock):", payload);
    showSuccessModal.value = true; // Muestra el modal de éxito
  } catch (err) {
    console.error(err);
    alert("Hubo un problema al guardar la entrada");
  }
}


//conectarse al backend
/*
async function saveEntry() {
  showConfirmationModal.value = false;

  const payload = {
    emotions: selectedEmotions.value,
    content: content.value.trim(),
    title: title.value.trim(),
    date: new Date().toISOString(),
  };

  try {
    const response = await fetch("/api/diary-entries/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Error al guardar entrada");
    }

    // Muestra el modal de éxito si todo salió bien
    showSuccessModal.value = true;
  } catch (err) {
    console.error(err);
    alert("Hubo un problema al guardar la entrada");
    // Opcional: mostrar un modal de error personalizado
  }
}
}*/

</script>