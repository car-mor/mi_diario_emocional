<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors">
    <div class="max-w-5xl mx-auto px-4 py-12">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full mb-6 shadow-lg bg-gradient-to-br from-[#5AA3CC] to-[#70BFE9]">
          <IconShieldLock class="w-10 h-10 text-white" stroke-width="2" />
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Aviso de Privacidad
        </h1>
        <p class="text-xl text-gray-600 mb-2">Mi Diario Emocional</p>
        <p class="text-sm text-gray-500">
          Fecha de última actualización: 20 de noviembre de 2025
        </p>
      </div>

      <!-- Introduction -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <p class="text-lg text-gray-700 leading-relaxed mb-4">
          En <span class="font-semibold text-[#70BFE9]">Mi Diario Emocional</span> (en adelante, "la Aplicación"), tu confianza y la protección de tus datos son nuestra máxima prioridad. Entendemos la naturaleza profundamente personal y sensible de la información que nos confías. Este Aviso de Privacidad explica de manera transparente cómo recopilamos, usamos y, sobre todo, cómo protegemos tus datos personales.
        </p>
        <div class="bg-[#70BFE9]/10 border-l-4 border-[#70BFE9] p-4 rounded">
          <p class="text-sm text-gray-700 flex items-start">
            <IconInfoCircle class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
            Este documento se emite en cumplimiento de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) de México.
          </p>
        </div>
      </div>

      <!-- Section 1: Identity -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconBuilding class="w-6 h-6 text-[#70BFE9]" />
          </div>
          1. Identidad y Domicilio del Responsable
        </h2>
        <div class="space-y-3 text-gray-700">
          <p>
            <span class="font-semibold">Mi Diario Emocional</span> (en adelante, "nosotros"), con domicilio en [Tu Domicilio Legal, Ciudad, Estado, C.P.], es el responsable del tratamiento (uso) de tus datos personales.
          </p>
          <div class="bg-gray-50 p-4 rounded-lg flex items-center">
            <IconMail class="w-5 h-5 text-[#70BFE9] mr-3 flex-shrink-0" />
            <div>
              <p class="text-sm font-medium text-gray-600">Contacto para Privacidad:</p>
              <a href="mailto:midiarioemocional_help@outlook.com" class="text-[#70BFE9] hover:text-[#5AA3CC] transition-colors">
                midiarioemocional_help@outlook.com
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 2: Data Collection -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconDatabase class="w-6 h-6 text-[#70BFE9]" />
          </div>
          2. Datos Personales que Recabamos
        </h2>

        <div class="space-y-6">
          <!-- A. Identification Data -->
          <div class="border-l-4 border-[#70BFE9] pl-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <IconUser class="w-5 h-5 mr-2 text-[#70BFE9]" />
              A. Datos de Identificación y Contacto (Para todos los usuarios)
            </h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                Nombre completo
              </li>
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                Correo electrónico
              </li>
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                Fecha de nacimiento (para verificación de mayoría de edad)
              </li>
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                Contraseña de acceso
              </li>
            </ul>
          </div>

          <!-- B. Verification Data -->
          <div class="border-l-4 border-[#5AA3CC] pl-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <IconCertificate class="w-5 h-5 mr-2 text-[#5AA3CC]" />
              B. Datos de Verificación (Exclusivo para Terapeutas)
            </h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#5AA3CC] flex-shrink-0 mt-0.5" />
                Cédula Profesional
              </li>
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-[#5AA3CC] flex-shrink-0 mt-0.5" />
                Clave Única de Registro de Población (CURP)
              </li>
            </ul>
          </div>

          <!-- C. Sensitive Data -->
          <div class="border-l-4 border-red-400 pl-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <IconAlertTriangle class="w-5 h-5 mr-2 text-red-500" />
              C. Datos Personales Sensibles (Exclusivo para Pacientes)
            </h3>
            <ul class="space-y-2 text-gray-700 mb-3">
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-red-400 flex-shrink-0 mt-0.5" />
                <span><strong>Contenido de Entradas del Diario:</strong> Los textos, títulos y emociones que registras voluntariamente.</span>
              </li>
              <li class="flex items-start">
                <IconPoint class="w-5 h-5 mr-2 text-red-400 flex-shrink-0 mt-0.5" />
                <span><strong>Datos de Salud Emocional:</strong> Las emociones seleccionadas y los resultados del análisis automatizado por IA de tus entradas.</span>
              </li>
            </ul>
            <div class="bg-red-50 p-4 rounded-lg">
              <p class="text-sm text-gray-700 flex items-start">
                <IconInfoCircle class="w-5 h-5 mr-2 text-red-500 flex-shrink-0 mt-0.5" />
                De acuerdo con la ley, tus entradas del diario son consideradas <strong>Datos Personales Sensibles</strong> ya que revelan tu estado de salud mental y emocional. Requerimos tu consentimiento explícito (que otorgas al aceptar este aviso) para su tratamiento.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 3: Purpose -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconTarget class="w-6 h-6 text-[#70BFE9]" />
          </div>
          3. Finalidades del Tratamiento de Datos
        </h2>

        <div class="space-y-6">
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <IconStarFilled class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Finalidades Primarias (Necesarias para el servicio)
            </h3>
            <ul class="space-y-3 text-gray-700">
              <li class="flex items-start">
                <IconCircleCheck class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                <span><strong>Generales:</strong> Crear y gestionar tu cuenta; verificar tu identidad; y proveer soporte técnico.</span>
              </li>
              <li class="flex items-start">
                <IconCircleCheck class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                <span><strong>Terapeutas:</strong> Validar tu estatus como profesional de la salud y generar tu código de vinculación único.</span>
              </li>
              <li class="flex items-start">
                <IconCircleCheck class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                <span><strong>Pacientes:</strong> Almacenar de forma segura tus entradas del diario; mostrarte tu historial; y generar los análisis y reportes de emociones derivados de tus textos.</span>
              </li>
              <li class="flex items-start">
                <IconCircleCheck class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
                <span><strong>Vinculación:</strong> Si (y solo si) un Paciente lo solicita explícitamente, transferir sus datos (entradas, análisis) al Terapeuta que ha seleccionado.</span>
              </li>
            </ul>
          </div>

          <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
            <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
              <IconShieldCheck class="w-5 h-5 mr-2 text-green-600" />
              Finalidades Secundarias (Opcionales)
            </h3>
            <p class="text-gray-700">
              No utilizaremos tus datos personales sensibles para finalidades secundarias (como marketing o publicidad). Tu paz mental es nuestra prioridad.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 4: Security -->
      <div class="bg-gradient-to-br from-[#5AA3CC] to-[#70BFE9] rounded-2xl shadow-lg p-6 md:p-8 mb-6 text-white">
        <h2 class="text-2xl font-bold mb-6 flex items-center">
          <IconLock class="w-8 h-8 mr-3" />
          4. Medidas de Seguridad Clave
        </h2>
        <p class="mb-6 text-white/90">
          Nos tomamos la seguridad de tus datos sensibles muy en serio. Hemos implementado las siguientes medidas técnicas y organizativas basadas en las mejores prácticas de la industria:
        </p>

        <div class="space-y-4">
          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5 hover:bg-white/20 transition-all">
            <h3 class="font-semibold text-lg mb-2 flex items-center">
              <IconKey class="w-6 h-6 mr-2" />
              Protección de Contraseña (Hashing)
            </h3>
            <p class="text-white/90 text-sm">
              Jamás almacenamos tu contraseña en texto plano. Usamos algoritmos de hashing seguros (los proporcionados por el framework Django) para que nadie, ni siquiera nuestro personal, pueda ver tu contraseña.
            </p>
          </div>

          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5 hover:bg-white/20 transition-all">
            <h3 class="font-semibold text-lg mb-2 flex items-center">
              <IconLockAccess class="w-6 h-6 mr-2" />
              Cifrado en Tránsito (SSL/TLS)
            </h3>
            <p class="text-white/90 text-sm">
              Toda la comunicación entre tu dispositivo y nuestros servidores viaja cifrada mediante el protocolo HTTPS. Esto impide que alguien pueda "interceptar" y leer tus entradas de diario mientras viajan por internet.
            </p>
          </div>

          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5 hover:bg-white/20 transition-all">
            <h3 class="font-semibold text-lg mb-2 flex items-center">
              <IconShieldCheck class="w-6 h-6 mr-2" />
              Autenticación Segura (JWT)
            </h3>
            <p class="text-white/90 text-sm">
              Tu sesión se gestiona mediante JSON Web Tokens (JWT), un estándar seguro que evita que tu contraseña se envíe repetidamente, protegiendo tu cuenta contra accesos no autorizados.
            </p>
          </div>

          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5 hover:bg-white/20 transition-all">
            <h3 class="font-semibold text-lg mb-2 flex items-center">
              <IconServer class="w-6 h-6 mr-2" />
              Seguridad del Backend (Django/DRF)
            </h3>
            <p class="text-white/90 text-sm">
              Nuestra API está construida sobre Django Rest Framework, que incluye defensas integradas contra las vulnerabilidades web más comunes, como Inyección SQL (para proteger la base de datos de tus entradas) y Cross-Site Scripting (XSS) (para proteger la visualización de tus datos).
            </p>
          </div>
        </div>
      </div>

      <!-- Section 5: Data Transfer -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconTransfer class="w-6 h-6 text-[#70BFE9]" />
          </div>
          5. Transferencia de Datos
        </h2>
        <div class="space-y-4 text-gray-700">
          <p>
            La única transferencia de datos sensibles que realizamos es aquella que el Paciente inicia y consiente explícitamente al vincularse con un Terapeuta. El Terapeuta está obligado (por estos términos y por su ética profesional) a tratar dicha información con estricta confidencialidad.
          </p>
          <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
            <p class="flex items-start">
              <IconShieldCheck class="w-5 h-5 mr-2 text-green-600 flex-shrink-0 mt-0.5" />
              Fuera de este caso, <strong>no vendemos, alquilamos ni compartimos</strong> tus datos personales con terceros.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 6: ARCO Rights -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconUserCheck class="w-6 h-6 text-[#70BFE9]" />
          </div>
          6. Derechos ARCO (Acceso, Rectificación, Cancelación y Oposición)
        </h2>
        <p class="text-gray-700 mb-4">Tienes derecho a:</p>
        <div class="grid md:grid-cols-2 gap-4 mb-6">
          <div class="bg-[#70BFE9]/5 p-4 rounded-lg">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconEye class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Acceder
            </h3>
            <p class="text-sm text-gray-600">A tus datos personales</p>
          </div>
          <div class="bg-[#70BFE9]/5 p-4 rounded-lg">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconEdit class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Rectificar
            </h3>
            <p class="text-sm text-gray-600">Si son inexactos o incompletos</p>
          </div>
          <div class="bg-[#70BFE9]/5 p-4 rounded-lg">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconTrash class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Cancelar
            </h3>
            <p class="text-sm text-gray-600">Cuando no sean necesarios</p>
          </div>
          <div class="bg-[#70BFE9]/5 p-4 rounded-lg">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconX class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Oponerte
            </h3>
            <p class="text-sm text-gray-600">Al uso para fines específicos</p>
          </div>
        </div>
        <div class="bg-blue-50 p-4 rounded-lg">
          <p class="text-gray-700 text-sm">
            <strong>Para ejercer estos derechos:</strong> Usa la opción "Eliminar mi cuenta" en tu perfil para cancelar tus datos, o contacta a
            <a href="mailto:midiarioemocional_help@outlook.com" class="text-[#70BFE9] hover:text-[#5AA3CC] transition-colors">
              midiarioemocional_help@outlook.com
            </a> para Acceso, Rectificación u Oposición.
          </p>
        </div>
      </div>

      <!-- Section 7: Changes -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconBell class="w-6 h-6 text-[#70BFE9]" />
          </div>
          7. Cambios al Aviso de Privacidad
        </h2>
        <p class="text-gray-700">
          Nos reservamos el derecho de efectuar modificaciones a este aviso. Cualquier cambio será notificado a través de la aplicación o por correo electrónico.
        </p>
      </div>

      <!-- Acceptance Section -->
       <template v-if="isRegistrationFlow">
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6" :class="{ 'ring-2 ring-red-500': showError }">
        <div class="flex items-start space-x-3">
          <input
            type="checkbox"
            id="acceptPrivacy"
            v-model="accepted"
            class="w-6 h-6 mt-1 text-[#70BFE9] border-gray-300 rounded focus:ring-[#70BFE9] focus:ring-2 cursor-pointer"
          >
          <label for="acceptPrivacy" class="cursor-pointer">
            <p class="font-semibold text-gray-900 mb-2">
              Consentimiento Explícito
            </p>
            <p class="text-sm text-gray-700 leading-relaxed">
              Al marcar esta casilla y crear una cuenta en "Mi Diario Emocional", manifiesto mi consentimiento explícito para el tratamiento de mis datos personales, incluidos los datos personales sensibles, de acuerdo con los términos establecidos en este Aviso de Privacidad. He leído, entendido y acepto todas las condiciones aquí descritas.
            </p>
          </label>
        </div>
        <div v-if="showError" class="mt-4 flex items-center text-red-600 text-sm">
          <IconAlertCircle class="w-5 h-5 mr-2" />
          Debes aceptar el Aviso de Privacidad para continuar.
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-end mb-8">
        <button
          type="button"
          @click="handleCancel"
          class="px-8 py-3 rounded-full border-2 border-gray-300 text-gray-700 font-semibold hover:bg-gray-50 transition-all"
        >
          Cancelar
        </button>
        <button
          type="button"
          @click="handleAccept"
          :disabled="!accepted"
          class="px-8 py-3 rounded-full font-semibold text-white shadow-lg transition-all flex items-center justify-center"
          :class="accepted ? 'bg-gradient-to-r from-[#5AA3CC] to-[#70BFE9] hover:shadow-xl hover:scale-105' : 'bg-gray-400 cursor-not-allowed'"
        >
          <IconCheck class="w-5 h-5 mr-2" />
          Aceptar y Continuar
        </button>
      </div>

      </template>

      <!-- Footer -->
      <div class="text-center text-gray-500 text-sm">
        <p class="flex items-center justify-center">
          <IconCopyright class="w-4 h-4 mr-1" />
          {{ currentYear }} Mi Diario Emocional. Todos los derechos reservados.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  IconShieldLock,
  IconInfoCircle,
  IconBuilding,
  IconMail,
  IconDatabase,
  IconUser,
  IconPoint,
  IconCertificate,
  IconAlertTriangle,
  IconTarget,
  IconStarFilled,
  IconCircleCheck,
  IconShieldCheck,
  IconLock,
  IconKey,
  IconLockAccess,
  IconServer,
  IconTransfer,
  IconUserCheck,
  IconEye,
  IconEdit,
  IconTrash,
  IconX,
  IconBell,
  IconAlertCircle,
  IconCheck,
  IconCopyright
} from '@tabler/icons-vue';

const router = useRouter();
const route = useRoute();
const accepted = ref<boolean>(false);
const showError = ref<boolean>(false);
const currentYear = computed(() => new Date().getFullYear());
const isRegistrationFlow = computed(() => route.query.flow === 'register');
const registrationType = computed(() => route.query.type);

const handleAccept = (): void => {
  if (!accepted.value) {
    showError.value = true;
    document.getElementById('acceptPrivacy')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  showError.value = false;
  router.push(`/terms-and-conditions?flow=register&type=${registrationType.value}`);
};

const handleCancel = (): void => {
  // Puedes redirigir a home o mostrar confirmación
  router.push({ name: 'register' });
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// También resetea el scroll si cambian los query params
watch(() => route.query, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>
