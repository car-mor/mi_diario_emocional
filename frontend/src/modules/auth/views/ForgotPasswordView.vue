<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
      <div class="flex items-center justify-center">
        <WomanHeart />
      </div>
<!-- Comentario para que reconozca el cambio main -->

      <div class="flex items-center justify-center">
        <div
          class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-600 p-8 shadow-lg border border-gray-100 dark:border-gray-500"
        >
          <ForgotPassword />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WomanHeart from '../components/WomanHeart.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
</script>
