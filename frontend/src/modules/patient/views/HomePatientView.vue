<template>
  <div class="flex h-screen">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden">
      <StreakAndTitle title="Inicio: Recursos de Autoayuda" :streakCount="2" />
      
      <div class="flex-1 p-6 overflow-y-auto">

        <div class="mb-8 relative bg-gradient-to-r overflow-hidden h-96 flex items-center justify-center">
          <img 
            src="https://img.europapress.es/fotoweb/fotonoticia_20220430132209_690.jpg" 
            alt="Artículo destacado" 
            class="w-4/5 h-full object-cover rounded-2xl opacity-100"
          />
          
          <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-10 text-white text-center w-full px-4">
            <router-link to="/article-weekly-patient">
              <button
                class="bg-[#7DBFF8] bg-opacity-50 p-3 rounded-lg hover:bg-[#3457B2] transition shadow-lg transition-colors text-white"
              >
                <h1 class="font-bold">Ver: Artículo de la semana</h1>
                  ¿Cómo superar el trauma de una ruptura? Una guía práctica. <b>Por: Silvia Congost</b>
              </button>
            </router-link>
          </div>

          <div class="hidden sm:flex absolute right-3.5 top-1/2 transform -translate-y-1/2 flex flex-col gap-4 z-10 ml-4">
            <button class="w-16 h-16 bg-[#B5D8B8] hover:bg-green-500 rounded-2xl flex items-center justify-center text-white shadow-lg transition-colors">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
            </button>
            
            <button class="w-16 h-16 bg-blue-300 hover:bg-blue-400 rounded-2xl flex items-center justify-center text-white shadow-lg transition-colors">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </button>
            
            <button class="w-16 h-16 bg-[#EDA1A1] hover:bg-red-400 rounded-2xl flex items-center justify-center text-white shadow-lg transition-colors">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="mb-8">
          <h3 class="text-xl font-semibold text-gray-800 mb-6">¿Te gustaría explorar nuevos temas? ¡Hagámoslo!</h3>
          
          <swiper
            :space-between="15"
            :centered-slides="true"
            :loop="false"
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
            <swiper-slide class="flex justify-center items-center">
  <router-link to="/video-carrusel-1-patient" class="block w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      <img 
        src="https://aprendemosjuntos.bbva.com/wp-content/uploads/2024/10/1024x512-01-MARIAN-ROJAS-2-CORTE.jpg" 
        alt="Video psicología 1" 
        class="w-full h-40 object-cover"
      />
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 mb-2">
          Video. Completa. Recupera tu mente, reconquista tu vida.
        </h4>
        <p class="text-sm text-gray-600">Marian Rojas-Estapé, psiquiatra y escritora.</p>
      </div>
    </div>
  </router-link>
</swiper-slide>

            <swiper-slide class="flex justify-center items-center">
  <router-link to="/audiobook-carrusel-2-patient" class="block w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      <img 
        src="https://static.wixstatic.com/media/2293b8_960d7feeb57d4eb592647ab51d334711~mv2.jpg/v1/fill/w_480,h_440,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/2293b8_960d7feeb57d4eb592647ab51d334711~mv2.jpg" 
        alt="Video psicología 1" 
        class="w-full h-40 object-cover"
      />
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 mb-2">
          Audiolibro - Hábitos Atómicos, Por James Clear
        </h4>
        <p class="text-sm text-gray-600">Un método sencillo y comprobado para desarrollar buenos hábitos y eliminar los malos.</p>
      </div>
    </div>
  </router-link>
</swiper-slide>


<swiper-slide class="flex justify-center items-center">
  <router-link to="/video-carrusel-1-patient" class="block w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      <img 
        src="https://aprendemosjuntos.bbva.com/wp-content/uploads/2024/10/1024x512-01-MARIAN-ROJAS-2-CORTE.jpg" 
        alt="Video psicología 1" 
        class="w-full h-40 object-cover"
      />
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 mb-2">
          Video. Completa. Recupera tu mente, reconquista tu vida.
        </h4>
        <p class="text-sm text-gray-600">Marian Rojas-Estapé, psiquiatra y escritora.</p>
      </div>
    </div>
  </router-link>
</swiper-slide>


<swiper-slide class="flex justify-center items-center">
  <router-link to="/video-carrusel-1-patient" class="block w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      <img 
        src="https://aprendemosjuntos.bbva.com/wp-content/uploads/2024/10/1024x512-01-MARIAN-ROJAS-2-CORTE.jpg" 
        alt="Video psicología 1" 
        class="w-full h-40 object-cover"
      />
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 mb-2">
          Video. Completa. Recupera tu mente, reconquista tu vida.
        </h4>
        <p class="text-sm text-gray-600">Marian Rojas-Estapé, psiquiatra y escritora.</p>
      </div>
    </div>
  </router-link>
</swiper-slide>


<swiper-slide class="flex justify-center items-center">
  <router-link to="/video-carrusel-1-patient" class="block w-full">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      <img 
        src="https://aprendemosjuntos.bbva.com/wp-content/uploads/2024/10/1024x512-01-MARIAN-ROJAS-2-CORTE.jpg" 
        alt="Video psicología 1" 
        class="w-full h-40 object-cover"
      />
      <div class="p-4">
        <h4 class="font-semibold text-gray-800 mb-2">
          Video. Completa. Recupera tu mente, reconquista tu vida.
        </h4>
        <p class="text-sm text-gray-600">Marian Rojas-Estapé, psiquiatra y escritora.</p>
      </div>
    </div>
  </router-link>
</swiper-slide>

            

            


          </swiper>

          
        </div>

        <div class="block md:hidden fixed right-6 top-1/2 transform -translate-y-1/2 flex flex-col gap-4 z-10">
          <button class="w-12 h-12 bg-green-500 hover:bg-green-600 rounded-lg flex items-center justify-center text-white shadow-lg transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
            </svg>
          </button>
          
          <button class="w-12 h-12 bg-blue-500 hover:bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-lg transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </button>
          
          <button class="w-12 h-12 bg-red-500 hover:bg-red-600 rounded-lg flex items-center justify-center text-white shadow-lg transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
        </div>

        <router-view />
      </div>
    </main>

    <UserProfile />
  </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
import StreakAndTitle from "../components/StreakAndTitlePatient.vue"
import UserProfile from "../components/PatientProfile.vue"
import router from "@/router";

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
  height: auto; /* El alto se ajusta al contenido */
  padding-bottom: 40px; /* Espacio para los puntos de paginación */
}
/* Estilo para que cada slide ocupe el espacio completo y centre la tarjeta */
.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>