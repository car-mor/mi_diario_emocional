<template>
    <h1 class="text-2xl font-bold text-[#7DBFF8] ">
        {{ title }}
    </h1>
</template>

<script setup lang="ts">
    defineProps<{ title: string }>()
</script>
