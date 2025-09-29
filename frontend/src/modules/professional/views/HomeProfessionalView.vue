<template>
    <div class="flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">
        <!-- Professional Header -->
        <ProfessionalHeader />
        <!-- Contenido principal -->
        
            <ProfessionalHome />
       
        <router-view />  
        <!-- Footer común -->
        <WelcomeFooter />
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import ProfessionalHeader from '../components/ProfessionalHeader.vue';
import WelcomeFooter from '@/modules/auth/components/WelcomeFooter.vue';
import ProfessionalHome from '@/modules/professional/components/ProfessionalHome.vue';

</script>