<template>
  <div class="flex flex-col items-center justify-center p-6">

    <!-- Paso 1: Seleccionar emociones (opcional) -->
    <div v-if="step === 1" class="w-full max-w-lg">
      <h2 class="text-xl font-semibold mb-4">Paso 1: Antes de escribir</h2>
      <p class="mb-4">¿Cómo te sientes en este momento?</p>
      <div class="flex justify-around mb-6">
        <label v-for="emo in emotions" :key="emo.value" class="flex flex-col items-center">
          <input type="checkbox" v-model="selectedEmotions" :value="emo.value" />
          <span>{{ emo.label }}</span>
        </label>
      </div>
      <button class="px-4 py-2 bg-blue-500 text-white rounded" @click="step++">Siguiente</button>
    </div>

    <!-- Paso 2: Escribir contenido del diario (obligatorio) -->
    <div v-if="step === 2" class="w-full max-w-lg">
      <h2 class="text-xl font-semibold mb-4">Paso 2: ¿Qué tal si escribimos un rato?</h2>
      <textarea
        v-model="content"
        class="w-full h-40 p-3 border rounded"
        placeholder="Hoy me siento..."
      ></textarea>
      <p v-if="contentError" class="text-red-500 text-sm mt-1">{{ contentError }}</p>
      <div class="flex justify-between mt-4">
        <button class="px-4 py-2 bg-gray-300 rounded" @click="step--">Atrás</button>
        <button class="px-4 py-2 bg-blue-500 text-white rounded" @click="validateContent">Siguiente</button>
      </div>
    </div>

    <!-- Paso 3: Agregar título (obligatorio) -->
    <div v-if="step === 3" class="w-full max-w-lg">
      <h2 class="text-xl font-semibold mb-4">Paso 3: Hora de agregar un título</h2>
      <input
        v-model="title"
        class="w-full p-3 border rounded mb-4"
        placeholder="Sin título..."
      />
      <p v-if="titleError" class="text-red-500 text-sm mt-1">{{ titleError }}</p>
      <div class="flex justify-between">
        <button class="px-4 py-2 bg-gray-300 rounded" @click="step--">Atrás</button>
        <button class="px-4 py-2 bg-green-500 text-white rounded" @click="validateAndSave">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const step = ref(1);
const emotions = [
  { value: "feliz", label: "😊" },
  { value: "triste", label: "😢" },
  { value: "ansioso", label: "😰" },
  { value: "enojado", label: "😡" },
  { value: "sorprendido", label: "😲" },
  { value: "cansado", label: "😴" },
];
const selectedEmotions = ref<string[]>([]);
const content = ref("");
const title = ref("");
const contentError = ref<string | null>(null);
const titleError = ref<string | null>(null);

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

function validateAndSave() {
  const cleanTitle = title.value.trim();

  // Si escribió titulo, validar
  if (cleanTitle.length > 0) {
    // Caracteres minimos
    if (cleanTitle.length < 3) {
      titleError.value = "El título debe tener al menos 3 caracteres.";
      return;
    }
    if (cleanTitle.length > 100) {
      titleError.value = "El título no puede exceder los 100 caracteres.";
      return;
    }
    // caracteres maximos
    const validCharacters = /^[a-zA-Z0-9\s.,!¡¿?_'-]*$/;
    if (!validCharacters.test(cleanTitle)) {
      titleError.value = "El título contiene caracteres no válidos.";
      return;
    }
  }else{
    // si no escribió titulo = error
    titleError.value = "Tu diario debe tener un título.";
    return;
  }
  // Si todo bien, guardar
  saveEntry();
}

/*
async function saveEntry() {
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

    if (!response.ok) throw new Error("Error al guardar entrada");

    alert("Entrada guardada con éxito 🎉");
    step.value = 1;
    selectedEmotions.value = [];
    content.value = "";
    title.value = "";
  } catch (err) {
    console.error(err);
    alert("Hubo un problema al guardar la entrada");
  }
}*/

//simulacion datos
async function saveEntry() {
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

    alert("Entrada guardada (mock) 🎉");
    step.value = 1;
    selectedEmotions.value = [];
    content.value = "";
    title.value = "";
  } catch (err) {
    console.error(err);
    alert("Hubo un problema al guardar la entrada (mock)");
  }
}
</script>