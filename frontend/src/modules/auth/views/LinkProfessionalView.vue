<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
    <div v-if="authStore.userProfile?.name" class="w-full max-w-md text-center">
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white">
  ¡Hola, {{ authStore.userProfile?.name }}!
</h1>
      <p class="mt-4 text-lg text-gray-600 dark:text-gray-300">
        Para continuar, necesitas vincular tu cuenta con un profesional.
      </p>
      <p class="mt-2 text-gray-500 dark:text-gray-400">
        Por favor, ingresa el código de enlace que te proporcionó tu terapeuta.
      </p>

      <div class="mt-8">
        <input
          v-model="linkCode"
          type="text"
          placeholder="Ingresa el código aquí"
          class="w-full p-4 text-center text-lg border-2 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          @keyup.enter="submitCode"
        />
        <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
      </div>

      <button
        @click="submitCode"
        :disabled="loading"
        class="mt-6 w-full px-6 py-3 bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold rounded-lg transition-colors duration-300 disabled:opacity-50"
      >
        {{ loading ? 'Vinculando...' : 'Vincular Cuenta' }}
      </button>

      <button
          @click="handleLogout"
          class="w-full px-6 py-2 bg-transparent text-gray-500 dark:text-gray-400 font-medium rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
        >
          Cerrar Sesión
        </button>
    </div>
  </div>

</template>

<script setup lang="ts">
// import { ref, onMounted } from 'vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { linkToProfessional } from '@/modules/professional/services/professionalServices';
import { isAxiosError } from 'axios';

const authStore = useAuthStore();
const router = useRouter();
// onMounted(() => {
//   console.log('Paso 3: Estado de userProfile CUANDO el componente se monta:', authStore.userProfile);
// });
const linkCode = ref('');
const loading = ref(false);
const error = ref<string | null>(null);

const submitCode = async () => {
  if (!linkCode.value.trim() || loading.value) return;

  loading.value = true;
  error.value = null;

  try {
    await linkToProfessional(linkCode.value.trim());

    await authStore.fetchUserProfile();
    router.push({ name: 'home-patient' });

  } catch (err: unknown) { // <-- 1. Cambiamos 'any' por 'unknown' (más seguro)
    console.error("Error al vincular:", err);

    // 2. Usamos el type guard para comprobar el error
    if (isAxiosError(err) && err.response) {
      // Dentro de este bloque, TypeScript sabe que 'err' es un AxiosError
      // y podemos acceder a 'err.response' de forma segura.
      error.value = err.response.data?.error || "Ocurrió un error. Verifica el código e inténtalo de nuevo.";
    } else {
      // Manejo para errores genéricos (ej. de red)
      error.value = "Ocurrió un error de conexión. Por favor, inténtalo más tarde.";
    }
  } finally {
    loading.value = false;
  }
};

const handleLogout = async () => {
  // La acción de logout en tu store ya se encarga de limpiar
  // todo y redirigir a la página de login.
  await authStore.logout();
};
</script>
