<template>
  <div class="dark:bg-gray-800 border-b border-gray-200 dark:border-gray-800 w-full pt-4 pb-4 px-4 sm:px-6">
    <div class="hidden lg:flex items-center justify-between">
      <div class="flex-grow flex justify-center">
        <h1 class="text-3xl font-bold text-[#7DBFF8]">
          {{ title }}
        </h1>
      </div>
      <div class="flex items-center space-x-1 text-orange-500 font-semibold flex-shrink-0">
        <span class="text-4xl">🔥</span>
        <span>{{ streakCount }} días de racha</span>
      </div>
    </div>
     <!-- Mobile -->
    <div class="lg:hidden flex flex-col items-center space-y-2">
      <h1 class="text-2xl font-bold text-[#7DBFF8] text-center">
        {{ title }}
      </h1>
      <div class="flex items-center space-x-1 text-orange-500 font-semibold">
        <span class="text-3xl">🔥</span>
        <span>{{ streakCount }} días de racha</span>
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