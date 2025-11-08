<template>
  <!-- <footer class="bg-gradient-to-r from-[#A7C4D5] to-[#B8C7CC] text-white"> -->
  <footer class="bg-[#70BFE8] dark:bg-gray-900 text-white">

    <div class="max-w-7xl mx-auto px-6 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Legal Links -->
        <div>
          <h6 class="font-bold mb-4 text-lg flex items-center">
            <IconFileText class="w-5 h-5 mr-2" />
            Legal
          </h6>
          <ul class="space-y-3">
            <li>
              <a
                href="#"
                @click.prevent="navigateTo('/terms-and-conditions')"
                class="group flex items-center text-white hover:text-white/80 transition-all duration-300"
              >
                <IconChevronRight class="w-4 h-4 mr-2 group-hover:translate-x-1 transition-transform" />
                <span class="relative">
                  Términos y Condiciones
                  <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-white group-hover:w-full transition-all duration-300"></span>
                </span>
              </a>
            </li>
            <li>
              <a
                @click.prevent="navigateTo('/privacy-policy')"
                class="group flex items-center text-white hover:text-white/80 transition-all duration-300"
              >
                <IconChevronRight class="w-4 h-4 mr-2 group-hover:translate-x-1 transition-transform" />
                <span class="relative">
                  Política de Privacidad
                  <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-white group-hover:w-full transition-all duration-300"></span>
                </span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact & Info -->
        <div>
          <h6 class="font-bold mb-4 text-lg flex items-center">
            <IconInfoCircle class="w-5 h-5 mr-2" />
            Información
          </h6>
          <ul class="space-y-3 text-sm">
            <li class="flex items-start">
              <IconBuilding class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
              <span>Proyecto académico 2025-B139 del IPN</span>
            </li>
            <li class="flex items-start">
              <IconShieldCheck class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
              <span>Adopción de directrices ISO/IEC 27001</span>
            </li>
            <li class="flex items-start">
              <IconMail class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
              <a
                href="mailto:midiarioemocional_help@outlook.com"
                class="hover:text-white/80 transition-colors break-all"
              >
                midiarioemocional_help@outlook.com
              </a>
            </li>
          </ul>
        </div>

        <!-- About & Social -->
        <div>
          <h6 class="font-bold mb-4 text-lg flex items-center">
            <IconHeartbeat class="w-5 h-5 mr-2" />
            Mi Diario Emocional
          </h6>
          <p class="text-sm mb-4 text-justify text-white/90 leading-relaxed">
            Una plataforma segura para el seguimiento emocional y la conexión terapéutica,
            diseñada con los más altos estándares de privacidad y seguridad.
          </p>
          <div class="flex gap-3">
            <a
              href="https://www.facebook.com/profile.php?id=61583184495757"
              class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all duration-300 hover:-translate-y-1"
              aria-label="Facebook"
            >
              <IconBrandFacebook class="w-5 h-5" />
            </a>
            <a
              href="https://www.instagram.com/midiario_emocional?igsh=MTFybjhmaHhuZWd1MA%3D%3D&utm_source=qr"
              class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all duration-300 hover:-translate-y-1"
              aria-label="Instagram"
            >
              <IconBrandInstagram class="w-5 h-5" />
            </a>
            <a
              href="https://www.youtube.com/@Mi-diario-emocional"
              class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all duration-300 hover:-translate-y-1"
              aria-label="YouTube"
              >
              <IconBrandYoutubeFilled class="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-12 pt-8 border-t border-white/20">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <p class="text-sm flex items-center">
            <IconCopyright class="w-4 h-4 mr-1" />
            {{ currentYear }} Mi Diario Emocional. Todos los derechos reservados.
          </p>
          <p class="text-sm text-white/75 flex items-center">
            Hecho con
            <IconHeart class="w-4 h-4 mx-1 text-red-400 fill-current" />
            para el bienestar emocional
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  IconFileText,
  IconChevronRight,
  IconInfoCircle,
  IconBuilding,
  IconShieldCheck,
  IconMail,
  IconHeartbeat,
  IconBrandFacebook,
  IconBrandInstagram,
  IconCopyright,
  IconHeart,
  IconBrandYoutubeFilled
} from '@tabler/icons-vue';

const router = useRouter();
const currentYear = computed(() => new Date().getFullYear());

const navigateTo = (path: string): void => {
  router.push(path);
};
</script>
