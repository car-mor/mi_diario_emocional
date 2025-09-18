<script setup lang="ts">
import { RouterView } from 'vue-router'
import WelcomeHeader from '@/modules/auth/components/WelcomeHeader.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <!--<WelcomeHeader />
      <!-- To do -->
    </div>
  </header>

  <RouterView />
</template>

<style scoped></style>
