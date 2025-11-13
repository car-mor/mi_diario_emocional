<template>
  <BackgroundWrapper>
    <div
      class="max-w-xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors duration-300"
    >
      <h2 class="text-2xl font-semibold mb-6 text-center text-[#70BFE9] dark:text-[#70BFE9]">
        Crear una cuenta para: Profesional de la Salud Mental
      </h2>

      <form v-if="step === 1" @submit.prevent="submitRegistration">
        <div class="space-y-4">
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Correo electrónico *</label
            >
            <div class="relative flex items-center">
              <IconMail class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.email"
                type="email"
                placeholder="Ingresa tu correo electrónico"
                @blur="validateEmail" class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
                :class="{
                  'border-red-500 dark:border-red-500 focus:ring-red-500': emailError,
                  'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !emailError
                }"
                required
              />
            </div>
            <p v-if="emailError" class="text-sm text-red-500 mt-2">{{ emailError }}</p>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Contraseña *</label
            >
            <div class="relative flex items-center">
              <IconLock class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.password"
                type="password"
                placeholder="Ingresa tu contraseña"
                class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
            <div
              v-if="form.password.length > 0"
              class="text-sm text-left text-gray-600 dark:text-gray-400 mt-2 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg space-y-1"
            >
              <p v-for="req in passwordValidation" :key="req.text" class="transition-colors flex items-center"
                :class="{'text-green-500 dark:text-green-400': req.met, 'text-red-500 dark:text-red-400': !req.met}">
                <span class="mr-2">{{ req.met ? '✓' : '✗' }}</span>
                <span>{{ req.text }}</span>
              </p>
            </div>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Vuelve a introducir tu contraseña *</label
            >
            <div class="relative flex items-center">
              <IconLock class="absolute left-4 text-gray-400 dark:text-gray-500" />
              <input
                v-model="form.confirmPassword"
                type="password"
                placeholder="Vuelve a introducir la contraseña"
                class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
            <div
              v-if="form.password !== form.confirmPassword && form.confirmPassword.length > 0"
              class="text-sm text-left text-gray-600 dark:text-gray-400 mt-2 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg space-y-1"
            >
              <p class="flex items-center text-red-500 dark:text-red-400">
                <span>Las contraseñas no coinciden.</span
              >
              </p>
            </div>
          </div>
           <p v-if="passwordError" class="text-sm text-red-500 mt-2">{{ passwordError }}</p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Nombre(s) *</label
              >
              <input
                v-model="form.name"
                type="text"
                placeholder="Ingresa tu nombre(s)"
                @blur="validateName" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': nameError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !nameError
              }"
              required
              />
              <p v-if="nameError" class="text-sm text-red-500 mt-2">{{ nameError }}</p>
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Primer apellido *</label
              >
              <input
                v-model="form.paternalLastName"
                type="text"
                placeholder="Ingresa tu primer apellido"
                @blur="validatePaternalLastName" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': paternalLastNameError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !paternalLastNameError
              }"
              required
              />
              <p v-if="paternalLastNameError" class="text-sm text-red-500 mt-2">{{ paternalLastNameError }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Segundo apellido</label
              >
              <input
                v-model="form.maternalLastName"
                type="text"
                placeholder="Ingresa tu segundo apellido"
                @blur="validateMaternalLastName" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': maternalLastNameError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !maternalLastNameError
              }"

              />
              <p v-if="maternalLastNameError" class="text-sm text-red-500 mt-2">{{ maternalLastNameError }}</p>
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Fecha de nacimiento *</label
              >
              <input
                v-model="form.dateOfBirth"
                type="date"
                @change="validateDateOfBirth" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': dateOfBirthError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !dateOfBirthError
              }"
              required
              />
              <p v-if="dateOfBirthError" class="text-sm text-red-500 mt-2">{{ dateOfBirthError }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Sexo *</label
              >
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              >
                <option value="" disabled>Selecciona el sexo...</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
              </select>
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Cédula profesional *</label
              >
              <input
                v-model="form.professionalLicense"
                type="text"
                placeholder="Ingresa tu No. de Cédula Profesional"
                @blur="validateLicense" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': licenseError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !licenseError
              }"
              required
              />
              <p v-if="licenseError" class="text-sm text-red-500 mt-2">{{ licenseError }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >CURP *</label
              >
              <input
                v-model="form.curp"
                type="text"
                placeholder="Ingresa tu CURP"
                @blur="validateCurp" class="w-full px-4 py-3 rounded-lg border bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2"
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': curpError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !curpError
              }"
              required
              />
              <p v-if="curpError" class="text-sm text-red-500 mt-2">{{ curpError }}</p>
            </div>
            <div class="relative">
              <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
                >Institución de egreso *</label
              >
              <input
                v-model="form.institution"
                type="text"
                placeholder="Ingresa tu Institución de procedencia"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
              />
            </div>
          </div>
          <div class="relative">
            <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2"
              >Carrera *</label
            >
            <input
              v-model="form.career"
              type="text"
              placeholder="Ingresa tu carrera o licenciatura"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              required
            />
          </div>

          <p class="text-sm text-gray-500 dark:text-gray-400 pt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            {{ loading ? 'Enviando solicitud...' : 'Enviar para Revisión' }}
          </button>
        </div>
      </form>

      <div v-else-if="step === 4" class="text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <IconCircleCheckFilled class="text-green-500 w-20 h-20 mb-4" />
          <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">
            ¡Gracias por completar el registro!
          </h3>
          <p class="text-gray-600 dark:text-gray-400 leading-relaxed text-center">
            Te notificaremos por correo cuando hayamos validado tus datos y cédula profesional para que puedas
            comenzar a usar la aplicación. Este proceso puede tardar de 1 a 3 días hábiles. Mientras tanto, puedes
            regresar al inicio de sesión y activar tu cuenta con el código que te enviamos por correo (Expira en 15 minutos).
          </p>
        </div>
        <button
          @click="goToLogin"
          class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
        >
          Ir a inicio de sesión
        </button>
      </div>
    </div>
  </BackgroundWrapper>

  <div
    v-if="errorPopup"
    class="fixed inset-0 flex items-center justify-center z-50"
    @click="closeErrorPopup"
  >
    <div
      class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl max-w-sm w-full text-center m-4"
      @click.stop
    >
      <div class="flex flex-col items-center justify-center">
        <IconCircleXFilled class="text-red-500 w-16 h-16 mb-4" />
        <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-100">Error</h3>
        <p class="text-gray-600 dark:text-gray-300 mb-4">{{ errorMessage }}</p>
        <button
          @click="closeErrorPopup"
          class="bg-red-500 text-white font-semibold py-2 px-6 rounded-lg hover:bg-red-600 transition-colors"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, type Ref, onMounted  } from 'vue'

import { useRouter, useRoute } from 'vue-router'
import { isAxiosError } from 'axios';
import * as AuthServices from '@/modules/auth/services/authServices';
import BackgroundWrapper from '@/modules/auth/components/BackgroundWrapper.vue'
import { IconMail, IconLock, IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-vue'

const router = useRouter()
const route = useRoute()

const step = ref(1) // 1 para el formulario, 4 para el mensaje de éxito
const loading = ref(false)
const errorPopup = ref(false)
const errorMessage = ref('')
const passwordError = ref('');
const emailError = ref('');
const curpError = ref('');
const licenseError = ref('');
const nameError = ref('');
const paternalLastNameError = ref('');
const maternalLastNameError = ref('');
const dateOfBirthError = ref('');
const hasAttemptedSubmit = ref(false);
const termsAccepted = ref(false);

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  name: '',
  paternalLastName: '',
  maternalLastName: '',
  dateOfBirth: '',
  gender: '', // 'sex' en el backend
  professionalLicense: '',
  curp: '',
  institution: '',
  career: '',
})

onMounted(() => {
  if (route.query.terms === 'true') {
    termsAccepted.value = true;
  } else {
    // Si intentan acceder a la URL de registro directamente,
    // los echamos a la página de bienvenida.
    router.push({ name: 'welcome' });
  }
});

// Función genérica para validar campos de texto (nombres, apellidos)
const validateTextField = (fieldValue: string, errorRef: Ref<string>, fieldName: string) => {
  const textRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/;
  const trimmedValue = fieldValue.trim(); // Usamos .trim() para la validación

  // 1. Validar "obligatorio" (SOLO SI SE INTENTÓ ENVIAR)
  if (hasAttemptedSubmit.value && !trimmedValue) {
    errorRef.value = `El ${fieldName} es obligatorio.`;
    return false;
  }

  // 2. Validar formato (SIEMPRE, si hay texto)
  if (trimmedValue && !textRegex.test(trimmedValue)) {
    errorRef.value = `El ${fieldName} solo puede contener letras y espacios.`;
    return false;
  }

  // 3. Longitud (SIEMPRE, si hay texto)
  if (trimmedValue && (trimmedValue.length < 2 || trimmedValue.length > 40)) {
    errorRef.value = `El ${fieldName} debe tener entre 2 y 40 caracteres.`;
    return false;
  }

  errorRef.value = '';
  return true;
};

const validateOptionalTextField = (fieldValue: string, errorRef: Ref<string>, fieldName: string) => {
  const textRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/;

  // 1. Validar formato (SOLO SI hay texto)
  if (fieldValue.trim() && !textRegex.test(fieldValue)) {
    errorRef.value = `El ${fieldName} solo puede contener letras y espacios.`;
    return false; // Falla
  }

  // 3. Longitud (SIEMPRE, si hay texto)
  if (fieldValue.trim() && (fieldValue.trim().length < 2 || fieldValue.trim().length > 40)) {
    errorRef.value = `El ${fieldName} debe tener entre 2 y 40 caracteres.`;
    return false; // Falla
  }

  // 2. Si está vacío, está bien (es opcional)
  errorRef.value = '';
  return true; // Pasa
};

const validateName = () => {
  validateTextField(form.name, nameError, 'nombre');
};
const validatePaternalLastName = () => {
  validateTextField(form.paternalLastName, paternalLastNameError, 'primer apellido');
};
const validateMaternalLastName = () => {
  validateOptionalTextField(form.maternalLastName, maternalLastNameError, 'segundo apellido');
};

// Función para validar la fecha de nacimiento
const validateDateOfBirth = () => {
  if (hasAttemptedSubmit.value && !form.dateOfBirth) {
    dateOfBirthError.value = 'La fecha de nacimiento es obligatoria.';
    return false;
  }

  // Si está vacío pero aún no se intenta enviar, no es un error.
  if (!form.dateOfBirth) {
    dateOfBirthError.value = '';
    return true; // No es un error "activo"
  }
  const birthDate = new Date(form.dateOfBirth);
  const today = new Date();

  // 1. Verificar si la fecha es futura
  if (birthDate > today) {
    dateOfBirthError.value = 'La fecha de nacimiento no puede ser en el futuro.';
    return;
  }

  // 2. Verificar si es mayor de 18 años
  const age = today.getFullYear() - birthDate.getFullYear();
  const monthDifference = today.getMonth() - birthDate.getMonth();
  const dayDifference = today.getDate() - birthDate.getDate();

  if (age > 120) {
    dateOfBirthError.value = 'La fecha de nacimiento no es válida.';
    return false;
  }

  // Ajuste si aún no ha cumplido años este año
  let is18 = false;
  if (age > 18) {
    is18 = true;
  } else if (age === 18) {
    if (monthDifference > 0) {
      is18 = true;
    } else if (monthDifference === 0 && dayDifference >= 0) {
      is18 = true;
    }
  }

  if (!is18) {
    dateOfBirthError.value = 'Debes ser mayor de 18 años para registrarte.';
  } else {
    dateOfBirthError.value = '';
  }
};


const passwordRequirements = [
  { regex: /[a-z]/, text: 'Al menos una letra minúscula' },
  { regex: /[A-Z]/, text: 'Al menos una letra mayúscula' },
  { regex: /\d/, text: 'Al menos un número' },
  { regex: /[@$!%*?&]/, text: 'Al menos un carácter especial (@$!%*?&)' },
  { regex: /^.{8,32}$/, text: 'Entre 8 y 32 caracteres' }
];

const passwordValidation = computed(() => {
  return passwordRequirements.map(req => ({
    ...req,
    // 👇 CAMBIO CLAVE: Usa 'form.password' en lugar de 'newPassword.value'
    met: req.regex.test(form.password)
  }));
});

const isPasswordValid = computed(() => passwordValidation.value.every(req => req.met));

// Función para validar el Correo
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // 1. Validar "obligatorio"
  if (hasAttemptedSubmit.value && !form.email) {
    emailError.value = 'El correo es obligatorio.';
    return false;
  }

  // 2. Validar formato (si hay texto)
  if (form.email && !emailRegex.test(form.email)) {
    emailError.value = 'Formato de correo inválido (ej. nombre@dominio.com)';
    return false;
  }

  emailError.value = '';
  return true;
};

// Función para validar la Cédula (asume 7-8 dígitos)
const validateLicense = () => {
  const licenseRegex = /^[0-9]{7,8}$/;
  // 1. Validar "obligatorio"
  if (hasAttemptedSubmit.value && !form.professionalLicense) {
    licenseError.value = 'La cédula es obligatoria.';
    return false;
  }

  // 2. Validar formato (si hay texto)
  if (form.professionalLicense && !licenseRegex.test(form.professionalLicense)) {
    licenseError.value = 'La cédula debe contener solo 7 u 8 números.';
    return false;
  }

  licenseError.value = '';
  return true;
};

// Función para validar la CURP (formato estándar de 18 caracteres)
const validateCurp = () => {
  const curpRegex = /^[A-Z]{4}[0-9]{6}[H|M][A-Z]{5}[A-Z0-9]{2}$/;
  // 1. Validar "obligatorio"
  if (hasAttemptedSubmit.value && !form.curp) {
    curpError.value = 'La CURP es obligatoria.';
    return false;
  }

  if (/[a-z]/.test(form.curp)) {
    curpError.value = 'La CURP debe estar en mayúsculas.';
    return false;
  }


  // 2. Validar formato (si hay texto)
  if (form.curp && !curpRegex.test(form.curp.toUpperCase())) {
    curpError.value = 'Formato de CURP inválido (deben ser 18 caracteres).';
    return false;
  }

  curpError.value = '';
  return true;
};

// Función única para enviar todo el formulario
const submitRegistration = async () => {
  hasAttemptedSubmit.value = true;
  passwordError.value = '';
  validateEmail();
  validateLicense();
  validateCurp();
  validateTextField(form.name, nameError, 'nombre');
  validateTextField(form.paternalLastName, paternalLastNameError, 'primer apellido');
  validateOptionalTextField(form.maternalLastName, maternalLastNameError, 'segundo apellido');
  validateDateOfBirth();
  if (!termsAccepted.value) {
    errorMessage.value = "Debe aceptar los términos antes de registrarse.";
    errorPopup.value = true;
    return;
  }

  // 1. Validación de contraseña en el frontend
  if (form.password !== form.confirmPassword) {
    passwordError.value = 'Las contraseñas no coinciden.';
    return;
  }

  if (!isPasswordValid.value) {
    passwordError.value = 'La contraseña no cumple con todos los requisitos de seguridad.';
    return;
  }

  if (
    emailError.value || licenseError.value || curpError.value || passwordError.value ||
    nameError.value || paternalLastNameError.value || maternalLastNameError.value || dateOfBirthError.value
  ) {
    return; // Detiene el envío
  }

  loading.value = true;

  // 2. Construir el payload EXACTAMENTE como lo espera tu ProfessionalSerializer
  const registrationPayload = {
      user: {
          email: form.email,
          password: form.password,
          name: form.name,
          paternal_last_name: form.paternalLastName,
          maternal_last_name: form.maternalLastName,
          date_of_birth: form.dateOfBirth,
          role: "professional",
          terms_accepted: termsAccepted.value
      },
      sex: form.gender,
      professional_license: form.professionalLicense,
      curp: form.curp,
      institution: form.institution,
      career: form.career,
      // El link_code se genera en el backend, no es necesario enviarlo
  };

  try {
    const response = await AuthServices.registerProfessional(registrationPayload);
    if (response.status === 201) {
        // Éxito: El profesional está pre-registrado y pendiente de revisión.
        step.value = 4; // Avanza a la pantalla de "Gracias, estamos revisando"
    }
  } catch (error: unknown) {
    if (isAxiosError(error) && error.response) {
      const data = error.response.data;
      let msg = 'Error de registro. Verifique sus datos.';

      // Manejo de errores anidados
      if (data.user && data.user.email) msg = `${data.user.email[0]}`;
      else if (data.professional_license) msg = `${data.professional_license[0]}`;
      else if (data.curp) msg = `${data.curp[0]}`;
      else if (data.detail) msg = data.detail;

      errorMessage.value = msg;
      errorPopup.value = true;
    } else {
      errorMessage.value = 'Ocurrió un error desconocido. Inténtelo de nuevo.';
      errorPopup.value = true;
    }
  } finally {
    loading.value = false;
  }
}

const goToLogin = () => {
  router.push('/login')
}

const closeErrorPopup = () => {
  errorPopup.value = false
  errorMessage.value = ''
}
</script>
