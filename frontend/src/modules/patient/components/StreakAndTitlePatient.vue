<template>
    <div class="w-full pt-13 pb-4">
        <!-- Desktop: título centrado con racha al lado -->
        <div class="hidden md:flex justify-center items-center relative">
            <h1 class="text-3xl font-bold text-[#7DBFF8]">
                {{ title }}
            </h1>
            <div class="absolute right-0 flex items-end space-x-1 text-orange-500 font-semibold px-7">
                <span class="text-4xl">🔥</span>
                <span class="">{{ streakCount }} días de racha</span>
            </div>
        </div>
        
        <!-- Mobile: título y racha apilados -->
        <div class="md:hidden flex flex-col items-center space-y-2">
            <h1 class="text-2xl font-bold text-[#7DBFF8] text-center">
                {{ title }}
            </h1>
            <div class="flex items-end space-x-1 text-orange-500 font-semibold">
                <span class="text-3xl">🔥</span>
                <span class="">{{ streakCount }} días de racha</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    defineProps<{ 
        title: string
        streakCount: number 
    }>()
</script>