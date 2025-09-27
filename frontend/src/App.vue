<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/store/auth' // Asegúrate de que la ruta es correcta

// Importa los tres componentes de header con sus nombres correspondientes
// import PacienteHeader from '@/modules/patient/components/PatientHeader.vue'
// import TerapeutaHeader from '@/modules/professional/components/ProfessionalHeader.vue'
import AnonymusHeader from '@/modules/auth/components/WelcomeHeader.vue'

const authStore = useAuthStore()
// Inicializa el tipo de usuario en 'anónimo' al cargar la aplicación
authStore.loginAs('terapeuta') // Cambia esto para probar diferentes tipos de usuario
</script>

<template>
  <header>
    <div class="wrapper">
      <PacienteHeader v-if="authStore.userType === 'paciente'" />
      <TerapeutaHeader v-else-if="authStore.userType === 'terapeuta'" />
      <AnonymusHeader v-else />
    </div>
  </header>

  <RouterView />
</template>
