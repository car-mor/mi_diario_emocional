<template>
    <aside
        class="hidden md:flex w-90 bg-white border-l border-gray-200 dark:bg-gray-800 dark:border-gray-700 p-6 flex-col"
    >
        <!-- Título -->
        <div class="flex flex-col items-center text-center">
            <h2 class="text-2xl mt-3 font-semibold text-gray-800 dark:text-gray-200">
                Perfil del usuario
            </h2>
        </div>

        <!-- Avatar -->
        <div class="mt-13 flex flex-col items-center text-center">
            <img
                src="https://i.pravatar.cc/150?img=38"
                alt="User avatar"
                class="w-40 h-40 rounded-xl object-cover"
            />
            <h2 class="mt-3 text-lg font-semibold text-gray-800 dark:text-gray-200">
                Alias de María
            </h2>
            <p class="text-sm text-gray-500">maria@correo.com</p>
        </div>

        <!-- Descripción -->
        <p class="mt-4 text-sm text-gray-600 dark:text-gray-400 text-center">
        Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui. Duis a lacus in arcu ultrices sodales vel in urna. Donec lacinia facilisis dui.
        </p>

        <!-- Botón Configurar cuenta -->
        <div class="mt-6 flex flex-col gap-3">
            <button
            type="submit"
            class="w-full bg-[#7DBFF8] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
            >
                Configurar cuenta
            </button>
        <!-- Botón Cerrar sesión -->
            <router-link
                to="/"
                class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
                Cerrar sesión
            </router-link>
        </div>
    </aside>
</template>
