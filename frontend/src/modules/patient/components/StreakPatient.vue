<template>
    <div class="flex items-center space-x-1 text-orange-500 font-semibold">
        <span class="text-2xl">🔥</span>
        <span>{{ count }} días de racha</span>
    </div>
</template>

<script setup lang="ts">
    defineProps<{ count: number }>()
</script>
