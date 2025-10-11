<template>
    <div class="flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">
        <!-- Professional Header -->
        <!-- Contenido principal -->
            <PatientDetails />
        <router-view />
        <!-- Footer común -->
        <WelcomeFooter />
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import WelcomeFooter from '@/modules/auth/components/WelcomeFooter.vue';
import PatientDetails from '@/modules/professional/components/PatientDetails.vue';

</script>
