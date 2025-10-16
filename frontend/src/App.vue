<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/store/auth';

import AnonymusHeader from '@/modules/auth/components/WelcomeHeader.vue';

const authStore = useAuthStore();

// Propiedad calculada: Verifica si el usuario está logueado con un rol específico.
// Si esta es TRUE, la vista cargada es el dashboard (Layout Padre).
const isAuthenticatedUser = computed(() => {
    const role = authStore.userType;
    return role === 'patient' || role === 'professional' || role === 'superuser';
});

onMounted(() => {
    // La verificación de la sesión se hace aquí al montar
    authStore.checkInitialAuth();
});
</script>

<template>
  <div :class="{ 'min-h-screen': !isAuthenticatedUser }">

    <header v-if="!isAuthenticatedUser" class="w-full">
      <div class="wrapper">
        <AnonymusHeader />
      </div>
    </header>

    <RouterView :class="{ 'flex-1': !isAuthenticatedUser }" />

  </div>
</template>
