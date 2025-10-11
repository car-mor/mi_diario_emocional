<template>
  <div class="h-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 p-4 text-center">

    <!-- Ilustración SVG -->
    <div class="w-64 h-64 mb-8">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="text-[#70BFE9] drop-shadow-lg">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" fill="currentColor"/>
        <path d="M12.5 7.5c0-.28-.22-.5-.5-.5s-.5.22-.5.5v5c0 .28.22.5.5.5s.5-.22.5-.5v-5zm0 7c0-.28-.22-.5-.5-.5s-.5.22-.5.5v.01c0 .28.22.5.5.5s.5-.22.5-.5v-.01z" fill="currentColor"/>
        <path d="M15.5 10.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm-7 0c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5z" fill="currentColor" opacity="0.6"/>
        <path d="M15.03 16.5c-.2-.2-.51-.2-.71 0l-4.63 4.63c-.2.2-.2.51 0 .71.2.2.51.2.71 0l4.63-4.63c.2-.2.2-.51 0-.71z" fill="currentColor" opacity="0.3"/>
      </svg>
    </div>

    <h1 class="text-6xl font-extrabold text-gray-800 dark:text-white drop-shadow-md">404</h1>
    <h2 class="text-2xl font-semibold text-gray-600 dark:text-gray-300 mt-2 mb-4">Página no encontrada</h2>
    <p class="text-gray-500 dark:text-gray-400 max-w-sm mb-2">
      Lo sentimos, la página que estás buscando no existe o ha sido movida.
    </p>

    <router-link
      to="/"
      class="px-8 py-3 bg-[#70BFE9] text-white font-semibold rounded-lg shadow-lg hover:bg-[#5a9cbf] transition-colors duration-300"
    >
      Regresar al Inicio
    </router-link>

  </div>
</template>
