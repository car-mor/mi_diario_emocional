<template>
      <div class="dark:bg-gray-900 flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">


    <main class="flex-1 flex flex-col overflow-hidden">
          <header>
      <ProfessionalHeader />
    </header>


      <div class="flex-1 p-6 overflow-y-auto">
        <ProfessionalHome />
        <router-view />
      </div>
    </main>
    <footer>
        <WelcomeFooter />
    </footer>
  </div>
</template>

<script setup lang="ts">
// 4. Imports necesarios para todos los componentes
import WelcomeFooter from '@/modules/auth/components/WelcomeFooter.vue';
import ProfessionalHeader from '../components/ProfessionalHeader.vue';
import ProfessionalHome from '../components/ProfessionalHome.vue';

</script>
