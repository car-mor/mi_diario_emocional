
<template>
    <div class="flex h-screen overflow-hidden">
        <main class="dark:bg-gray-800 flex-1 flex flex-col">

            <div class="lg:hidden flex-1 flex flex-col">
                <PatientProfileMobile />
            </div>

            <div class="hidden lg:flex flex-1 items-center justify-center p-8">
                <div class="text-center max-w-md">
                    </div>
            </div>

        </main>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
// Importa tus componentes internos aquí:
import PatientProfileMobile from "../components/PatientProfileMobile.vue";

const router = useRouter();

// Lógica de detección de pantalla (debe ser refactorizada para usar el router guard si es posible)
const mql = window.matchMedia('(min-width: 1024px)');

function handleMediaQuery(event: MediaQueryListEvent) {
    // Si la condición de pantalla grande se vuelve TRUE, redirigir
    if (event.matches) {
        // Redirige al home-patient (donde está el layout de escritorio)
        router.replace({ name: 'home-patient' });
    }
}

onMounted(() => {
    // Verificación inicial: Si al cargar es grande, redirige
    if (mql.matches) {
        router.replace({ name: 'home-patient' });
    }

    // Escuchar el cambio de tamaño
    mql.addEventListener('change', handleMediaQuery);
});

onUnmounted(() => {
    // Limpiar el listener
    mql.removeEventListener('change', handleMediaQuery);
});
</script>
