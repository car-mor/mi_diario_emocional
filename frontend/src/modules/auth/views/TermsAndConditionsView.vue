<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors">
    <div class="max-w-5xl mx-auto px-4 py-12">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full mb-6 shadow-lg bg-gradient-to-br from-[#5AA3CC] to-[#70BFE9]">
          <IconFileText class="w-10 h-10 text-white" stroke-width="2" />
        </div>
        <h1 class="text-4xl md:text-5xl font-bold dark:text-[#70BFE9] text-gray-900 mb-4">
          Términos y Condiciones de Uso
        </h1>
        <p class="text-xl text-gray-600 mb-2 dark:text-[#70BFE9]">Mi Diario Emocional</p>
        <p class="text-sm text-gray-500 dark:text-[#70BFE9]">
          Fecha de entrada en vigor: 20 de noviembre de 2025
        </p>
      </div>

      <!-- Introduction -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <p class="text-lg text-gray-700 leading-relaxed">
          Bienvenidos a <span class="font-semibold text-[#70BFE9]">Mi Diario Emocional</span>, en adelante, "la Aplicación".
          Estos Términos y Condiciones ("Términos") rigen tu acceso y uso de nuestra aplicación y servicios.
          Al crear una cuenta o utilizar nuestra Aplicación, aceptas cumplir con estos Términos.
        </p>
      </div>

      <!-- Section 1: Acceptance -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconCheck class="w-6 h-6 text-[#70BFE9]" />
          </div>
          1. Aceptación de los Términos
        </h2>
        <div class="space-y-3 text-gray-700">
          <p>
            Debes ser mayor de 18 años para crear una cuenta y utilizar esta Aplicación.
            Al marcar la casilla <strong>"Acepto los Términos y Condiciones y el Aviso de Privacidad"</strong> durante el registro,
            declaras que eres mayor de edad y aceptas estos Términos en su totalidad.
          </p>
          <div class="bg-[#70BFE9]/10 border-l-4 border-[#70BFE9] p-4 rounded flex items-start">
            <IconAlertCircle class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
            <span class="text-sm">Edad mínima requerida: 18 años</span>
          </div>
        </div>
      </div>

      <!-- Section 2: Service Description -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconClipboardText class="w-6 h-6 text-[#70BFE9]" />
          </div>
          2. Descripción del Servicio
        </h2>
        <div class="space-y-4 text-gray-700">
          <p>
            <span class="font-semibold text-[#70BFE9]">"Mi Diario Emocional"</span> es una herramienta digital diseñada para ayudarte a registrar y reflexionar sobre tus emociones.
            El servicio permite a los usuarios (en adelante, "Pacientes") escribir entradas de diario personales.
          </p>
          <div class="bg-blue-50 p-4 rounded-lg flex items-start">
            <IconUsers class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
            <p class="text-sm">
              <strong>Vinculación obligatoria:</strong> La Aplicación permite a los Pacientes vincularse con un profesional verificado (en adelante, "Terapeuta")
              para compartir sus entradas y facilitar un proceso terapéutico.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 3: Medical Disclaimer - IMPORTANT -->
      <div class="bg-red-50 border-2 border-red-300 rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-red-700 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-red-200 flex items-center justify-center mr-3">
            <IconAlertTriangle class="w-6 h-6 text-red-700" />
          </div>
          3. ¡Importante! Descargo de Responsabilidad Médica
        </h2>

        <div class="bg-white rounded-xl p-5 mb-4 border-l-4 border-red-500">
          <p class="text-lg font-bold text-red-700 mb-2 flex items-center">
            <IconAlertOctagon class="w-6 h-6 mr-2" />
            "Mi Diario Emocional" NO es un servicio médico ni de emergencia.
          </p>
        </div>

        <div class="space-y-4">
          <div class="bg-white rounded-xl p-5">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconStethoscope class="w-5 h-5 mr-2 text-red-600" />
              No es un Sustituto de Terapia
            </h3>
            <p class="text-gray-700 text-sm">
              La Aplicación es una herramienta de autoayuda y seguimiento. No sustituye el consejo, diagnóstico o tratamiento
              de un profesional de la salud mental calificado.
            </p>
          </div>

          <div class="bg-white rounded-xl p-5">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconPhone class="w-5 h-5 mr-2 text-red-600" />
              No es un Servicio de Crisis
            </h3>
            <p class="text-gray-700 text-sm mb-2">
              Si estás experimentando una crisis de salud mental, pensamientos suicidas o te encuentras en una situación de emergencia,
              por favor, <strong>contacta a los servicios de emergencia de tu localidad (como el 911) inmediatamente</strong>.
              La Aplicación no está diseñada para manejar crisis de emergencia.
            </p>
            <div class="bg-red-100 p-3 rounded mt-2">
              <p class="text-sm font-semibold text-red-700 flex items-center">
                <IconPhoneCall class="w-4 h-4 mr-2" />
                Emergencias: Llama al 911
              </p>
            </div>
          </div>

          <div class="bg-white rounded-xl p-5">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconRobot class="w-5 h-5 mr-2 text-red-600" />
              Análisis de IA
            </h3>
            <p class="text-gray-700 text-sm">
              Las emociones detectadas por nuestro análisis de IA son estimaciones algorítmicas y
              <strong>no constituyen un diagnóstico clínico de ningún tipo</strong>.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 4: User Accounts -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconUserCircle class="w-6 h-6 text-[#70BFE9]" />
          </div>
          4. Cuentas de Usuario y Seguridad
        </h2>
        <div class="space-y-4">
          <div class="border-l-4 border-[#70BFE9] pl-4">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconLock class="w-5 h-5 mr-2 text-[#70BFE9]" />
              Tu Cuenta
            </h3>
            <p class="text-gray-700 text-sm">
              Eres responsable de mantener la confidencialidad de tu contraseña.
            </p>
          </div>

          <div class="border-l-4 border-[#5AA3CC] pl-4">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconCertificate class="w-5 h-5 mr-2 text-[#5AA3CC]" />
              Cuentas de Terapeutas
            </h3>
            <p class="text-gray-700 text-sm">
              Los Terapeutas deben proporcionar información verídica (Cédula Profesional, CURP) para su validación.
              Nos reservamos el derecho de rechazar o suspender cuentas de Terapeutas que no puedan ser validadas.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 5: Patient-Therapist Link -->
      <div class="bg-gradient-to-br from-[#5AA3CC] to-[#70BFE9] rounded-2xl shadow-lg p-6 md:p-8 mb-6 text-white">
        <h2 class="text-2xl font-bold mb-4 flex items-center">
          <IconLink class="w-8 h-8 mr-3" />
          5. Vinculación entre Paciente y Terapeuta
        </h2>
        <p class="mb-6 text-white/90">
          Este es el núcleo de la funcionalidad de la Aplicación:
        </p>

        <div class="space-y-4">
          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5">
            <h3 class="font-semibold text-lg mb-3 flex items-center">
              <IconUser class="w-6 h-6 mr-2" />
              Para Pacientes
            </h3>
            <p class="text-white/90 text-sm leading-relaxed">
              <strong>Tú tienes el control total.</strong> Al usar el "Código de Vínculación" de un Terapeuta, otorgas tu consentimiento
              explícito e informado para que dicho Terapeuta tenga acceso completo a todas tus entradas del diario
              (pasadas, presentes y futuras) mientras la vinculación esté activa.
              Puedes desvincularte de tu Terapeuta en cualquier momento desde tu perfil, revocando su acceso inmediatamente.
            </p>
          </div>

          <div class="bg-white/10 backdrop-blur-sm rounded-xl p-5">
            <h3 class="font-semibold text-lg mb-3 flex items-center">
              <IconStethoscope class="w-6 h-6 mr-2" />
              Para Terapeutas
            </h3>
            <p class="text-white/90 text-sm leading-relaxed">
              Al aceptar la vinculación, te comprometes a mantener la más estricta confidencialidad sobre los datos de tus pacientes,
              de acuerdo con tu ética profesional y las leyes de protección de datos aplicables.
              <strong>El uso indebido de la información del paciente resultará en la terminación inmediata y permanente de tu cuenta.</strong>
            </p>
          </div>
        </div>
      </div>

      <!-- Section 6: Content Ownership -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconCopyright class="w-6 h-6 text-[#70BFE9]" />
          </div>
          6. Propiedad del Contenido
        </h2>
        <div class="bg-green-50 border-l-4 border-green-500 p-5 rounded-lg">
          <p class="text-gray-700 flex items-start">
            <IconShieldCheck class="w-5 h-5 mr-2 text-green-600 flex-shrink-0 mt-0.5" />
            <span>
              <strong>Tú (el Paciente) eres el propietario</strong> de todo el contenido que escribes en tu diario.
              Nosotros no reclamamos propiedad sobre tus entradas. Solo te otorgamos una licencia para usar la aplicación
              y almacenar ese contenido.
            </span>
          </p>
        </div>
      </div>

      <!-- Section 7: Prohibited Conduct -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center mr-3">
            <IconBan class="w-6 h-6 text-red-600" />
          </div>
          7. Conducta Prohibida
        </h2>
        <p class="text-gray-700 mb-4">Te comprometes a no usar la Aplicación para:</p>
        <div class="space-y-3">
          <div class="flex items-start bg-red-50 p-4 rounded-lg">
            <IconX class="w-5 h-5 mr-2 text-red-500 flex-shrink-0 mt-0.5" />
            <span class="text-gray-700 text-sm">
              Subir contenido ilegal, difamatorio o que incite al odio.
            </span>
          </div>
          <div class="flex items-start bg-red-50 p-4 rounded-lg">
            <IconX class="w-5 h-5 mr-2 text-red-500 flex-shrink-0 mt-0.5" />
            <span class="text-gray-700 text-sm">
              Intentar acceder sin autorización a las cuentas de otros usuarios.
            </span>
          </div>
          <div class="flex items-start bg-red-50 p-4 rounded-lg">
            <IconX class="w-5 h-5 mr-2 text-red-500 flex-shrink-0 mt-0.5" />
            <span class="text-gray-700 text-sm">
              Intentar "hackear" o comprometer la seguridad de la Aplicación.
            </span>
          </div>
        </div>
      </div>

      <!-- Section 8: Account Termination -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconLogout class="w-6 h-6 text-[#70BFE9]" />
          </div>
          8. Terminación de la Cuenta
        </h2>
        <div class="space-y-4">
          <div class="border-l-4 border-blue-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconUserCheck class="w-5 h-5 mr-2 text-blue-600" />
              Por tu parte
            </h3>
            <p class="text-gray-700 text-sm">
              Puedes eliminar tu cuenta en cualquier momento desde tu perfil.
              Esto eliminará permanentemente todos tus datos, incluidas tus entradas de diario.
            </p>
          </div>

          <div class="border-l-4 border-orange-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center">
              <IconShieldX class="w-5 h-5 mr-2 text-orange-600" />
              Por nuestra parte
            </h3>
            <p class="text-gray-700 text-sm">
              Nos reservamos el derecho de suspender o eliminar tu cuenta si violas gravemente estos Términos.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 9: Modifications -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconEdit class="w-6 h-6 text-[#70BFE9]" />
          </div>
          9. Modificaciones a los Términos
        </h2>
        <p class="text-gray-700 flex items-start">
          <IconBell class="w-5 h-5 mr-2 text-[#70BFE9] flex-shrink-0 mt-0.5" />
          Podemos actualizar estos Términos ocasionalmente. Te notificaremos de cambios importantes por correo electrónico
          o a través de un aviso en la Aplicación.
        </p>
      </div>

      <!-- Section 10: Applicable Law -->
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <div class="w-10 h-10 rounded-lg bg-[#70BFE9]/10 flex items-center justify-center mr-3">
            <IconScale class="w-6 h-6 text-[#70BFE9]" />
          </div>
          10. Ley Aplicable
        </h2>
        <div class="bg-gray-50 p-5 rounded-lg flex items-start">
          <IconFlag class="w-6 h-6 mr-3 text-green-600 flex-shrink-0" />
          <p class="text-gray-700">
            Estos Términos se regirán e interpretarán de acuerdo con las leyes de los
            <strong>Estados Unidos Mexicanos</strong>.
          </p>
        </div>
      </div>

      <!-- Acceptance Section -->
       <template v-if="isRegistrationFlow">
      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-6" :class="{ 'ring-2 ring-red-500': showError }">
        <div class="flex items-start space-x-3">
          <input
            type="checkbox"
            id="acceptTerms"
            v-model="accepted"
            class="w-6 h-6 mt-1 text-[#70BFE9] border-gray-300 rounded focus:ring-[#70BFE9] focus:ring-2 cursor-pointer"
          >
          <label for="acceptTerms" class="cursor-pointer">
            <p class="font-semibold text-gray-900 mb-2">
              Acepto los Términos y Condiciones
            </p>
            <p class="text-sm text-gray-700 leading-relaxed">
              Al marcar esta casilla, declaro que soy mayor de 18 años, he leído, entendido y acepto completamente
              estos Términos y Condiciones de Uso de "Mi Diario Emocional". Comprendo especialmente el descargo de
              responsabilidad médica y las condiciones de vinculación entre paciente y terapeuta.
            </p>
          </label>
        </div>
        <div v-if="showError" class="mt-4 flex items-center text-red-600 text-sm">
          <IconAlertCircle class="w-5 h-5 mr-2" />
          Debes aceptar los Términos y Condiciones para continuar.
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-end mb-8">
        <button
          type="button"
          @click="handleCancel"
          class="px-8 py-3 rounded-full border-2 border-gray-300 text-gray-700 font-semibold hover:bg-gray-50 transition-all"
        >
          Volver
        </button>
        <button
          type="button"
          @click="handleAccept"
          :disabled="!accepted"
          class="px-8 py-3 rounded-full font-semibold text-white shadow-lg transition-all flex items-center justify-center"
          :class="accepted ? 'bg-gradient-to-r from-[#5AA3CC] to-[#70BFE9] hover:shadow-xl hover:scale-105' : 'bg-gray-400 cursor-not-allowed'"
        >
          <IconCheck class="w-5 h-5 mr-2" />
          Aceptar y Finalizar
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
  IconFileText,
  IconCheck,
  IconAlertCircle,
  IconClipboardText,
  IconUsers,
  IconAlertTriangle,
  IconAlertOctagon,
  IconStethoscope,
  IconPhone,
  IconPhoneCall,
  IconRobot,
  IconUserCircle,
  IconLock,
  IconCertificate,
  IconLink,
  IconUser,
  IconCopyright,
  IconShieldCheck,
  IconBan,
  IconX,
  IconLogout,
  IconUserCheck,
  IconShieldX,
  IconEdit,
  IconBell,
  IconScale,
  IconFlag
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
    // Scroll to checkbox
    document.getElementById('acceptTerms')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  showError.value = false;

  if (registrationType.value === 'professional') {
    router.push({ name: 'register-professional', query: { terms: 'true' } });
  } else {
    router.push({ name: 'register-patient', query: { terms: 'true' } });
  }
};

const handleCancel = (): void => {
  // Volver al aviso de privacidad, MANTENIENDO EL QUERY Y EL TIPO
  router.push(`/privacy-policy?flow=register&type=${registrationType.value}`);
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// También resetea el scroll si cambian los query params
watch(() => route.query, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>
