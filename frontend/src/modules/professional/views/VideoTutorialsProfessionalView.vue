<template>
    <div class="flex flex-col min-h-screen grid grid-rows-[auto_1fr_auto] min-h-screen">
        <!-- Contenido principal -->
        <VideoTutorialsProfessional />

        <router-view />
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import VideoTutorialsProfessional from '@/modules/professional/components/VideoTutorialsProfessional.vue';

</script>
