<template>
    <div class="flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">
        <!-- Professional Header -->
        <!-- Contenido principal -->
            <ManagePatients />
        <router-view />
        <!-- Footer común -->
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import ManagePatients from '@/modules/professional/components/PatientManagement.vue';

</script>

