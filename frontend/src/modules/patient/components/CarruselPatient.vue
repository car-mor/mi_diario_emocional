<template>
    <swiper
            :space-between="15"
            :centered-slides="false"
            :loop="true"
            :pagination="{ clickable: true }"
            :navigation="true"
            :modules="[Navigation, Pagination, Scrollbar, A11y]"
            :breakpoints="{
                '640': {
                    slidesPerView: 2,
                    spaceBetween: 20,
                },
                '768': {
                    slidesPerView: 3,
                    spaceBetween: 30,
                },
                '1024': {
                    slidesPerView: 4,
                    spaceBetween: 40,
                },
            }"
    class="mySwiper"
    >
    <!-- Slide 1  Video - Marian Rojas-Stapé -->
    <swiper-slide class="flex justify-center items-center">
        <router-link to="/video-carrusel-1-patient" class="block w-full">
            <div class="dark:bg-gray-900 transition-colors bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                <img
                    src="https://aprendemosjuntos.bbva.com/wp-content/uploads/2024/10/1024x512-01-MARIAN-ROJAS-2-CORTE.jpg"
                    alt="Video psicología 1"
                    class="w-full h-40 object-cover"
                />
                <div class="p-4 h-40">
                    <h4 class="dark:text-gray-200 font-semibold text-gray-800 mb-2">
                        Video. Completa. Recupera tu mente, reconquista tu vida.
                    </h4>
                    <p class="dark:text-gray-400 text-sm text-gray-600">Marian Rojas-Estapé, psiquiatra y escritora.</p>
                </div>
            </div>
        </router-link>
    </swiper-slide>
    <!-- Slide 2  Audiolibro - Hábitos Atómicos -->
    <swiper-slide class="flex justify-center items-center">
        <router-link to="/audiobook-carrusel-2-patient" class="block w-full">
            <div class="bg-white dark:bg-gray-900 transition-colors rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                <img
                    src="https://imgs.search.brave.com/SOM_j95Q5ZNePD01qAUPPlYFHCK_U5iuEGWW1X614Rc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9odHRw/Mi5tbHN0YXRpYy5j/b20vRF9RX05QXzJY/Xzk4OTgyMi1NTFU3/NzMzMTYwNDgyNF8w/NzIwMjQtVi53ZWJw"
                    alt="Audiolibro 1"
                    class="w-full h-40 object-cover"
                />
                <div class="p-4 h-40">
                    <h4 class="dark:text-gray-200 font-semibold text-gray-800 mb-2">
                        Audiolibro - los Cuatro Acuerdos, Por Don Miguel Ruiz.
                    </h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">Es un ensayo sobre la libertad personal y cómo liberarnos de creencias limitantes.</p>
                </div>
            </div>
        </router-link>
    </swiper-slide>
    <!-- Slide 3  Podcast - Meditación -->
    <swiper-slide class="flex justify-center items-center">
        <router-link to="/meditation-carrusel-3-patient" class="block w-full">
            <div class="dark:bg-gray-900 transition-colorsbg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                <img
                    src="https://us.123rf.com/450wm/maxoidos/maxoidos1609/maxoidos160900021/65880231-pyramid-of-stones-for-meditation-lying-on-sea-coast-at-sunset.jpg"
                    alt="Podcast meditación"
                    class="w-full h-40 object-cover"
                />
                <div class="p-4 h-40">
                    <h4 class="dark:text-gray-200 font-semibold text-gray-800 mb-2">
                        Podcast. Vamos a meditar.
                    </h4>
                    <p class="dark:text-gray-400 text-sm text-gray-600">Por Glenda Yoga - Toma un momento para calmar tu mente.</p>
                </div>
            </div>
        </router-link>
    </swiper-slide>
    <!-- Slide 4  Video - Helena Echeverría -->
    <swiper-slide class="flex justify-center items-center">
        <router-link to="/video-carrusel-4-patient" class="block w-full">
            <div class="dark:bg-gray-900 transition-colors bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                <img
                    src="https://helenaecheverria.com/wp-content/uploads/2020/08/fotos.png"
                    alt="Video psicología 2"
                    class="w-full h-40 object-cover"
                />
                <div class="p-4 h-40">
                    <h4 class="dark:text-gray-200 font-semibold text-gray-800 mb-2">
                        Video. Cómo Regular y Gestionar Emociones Con Mindfulness.
                    </h4>
                    <p class="dark:text-gray-400 text-sm text-gray-600">Helena Echeverría, psicóloga y coach. Especialista en ansiedad.</p>
                </div>
            </div>
        </router-link>
    </swiper-slide>
    <!-- Slide 5  Video Conferencia - Fernando Lemarroy -->
    <swiper-slide class="flex justify-center items-center">
        <router-link to="/conference-carrusel-5-patient" class="block w-full">
            <div class="dark:bg-gray-900 transition-colors bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                <img
                    src="https://i.ytimg.com/vi/_9agX3gY1jU/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGE0gLyh_MA8=&rs=AOn4CLC6m93WxUVTjkOf521075DeoY2-og"
                    alt="Conferencia 1"
                    class="w-full h-40 object-cover"
                />
                <div class="p-4 h-40">
                    <h4 class="dark:text-gray-200 font-semibold text-gray-800 mb-2">
                        Video Conferencia. Salud mental, la clase que nadie nos dió.
                    </h4>
                    <p class="dark:text-gray-400 text-sm text-gray-600">Fernando Lemarroy | TEDxTecdeMty.</p>
                </div>
            </div>
        </router-link>
    </swiper-slide>
    </swiper>
</template>

<script setup lang="ts">
// Importar Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue';

// Importar Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

// Importar modules que necesitas (navegación, paginación, etc.)
import { Navigation, Pagination, Scrollbar, A11y } from 'swiper/modules';
</script>

<style scoped>
/* Estilos opcionales para customizar el carrusel */
.swiper {
    width: 100%; /* Asegura que ocupe todo el ancho disponible */
    height: 100%; /* El alto se ajusta al contenido */
    padding-bottom: 40px; /* Espacio para los puntos de paginación */
}
/* Estilo para que cada slide ocupe el espacio completo y centre la tarjeta */
.swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
