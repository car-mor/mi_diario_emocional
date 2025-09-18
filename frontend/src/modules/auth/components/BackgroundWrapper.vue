<!-- src/components/BackgroundWrapper.vue -->
<template>
  <div
    class="relative min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors overflow-hidden"
  >
    <!-- Círculo superior izquierdo (medio fuera del contenedor) -->
    <div
      aria-hidden="true"
      class="absolute -left-24 -top-20 w-64 h-64 md:-left-40 md:-top-24 md:w-80 md:h-80 rounded-full bg-[#70BFE9] pointer-events-none"
      style="filter: none"
    />

    <!-- Círculo inferior derecho (medio fuera del contenedor) -->
    <div
      aria-hidden="true"
      class="absolute -right-24 -bottom-20 w-64 h-64 md:-right-40 md:-bottom-24 md:w-80 md:h-80 rounded-full bg-[#70BFE9] pointer-events-none"
      style="filter: none"
    />

    <!-- Contenido sobre el fondo. Ajusta padding/width según tu layout -->
    <div class="relative z-10 container mx-auto px-6 py-12">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// Componente puramente presentacional; sin lógica por ahora.
// Puedes añadir props (por ejemplo color, tamaño) si quieres hacerlo dinámico.
</script>
