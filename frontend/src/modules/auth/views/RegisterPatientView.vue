<template>
  <BackgroundWrapper>
    <div
      class="max-w-5xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors duration-300"
    >
      <h2 class="text-2xl font-semibold mb-6 text-center text-[#70BFE9] dark:text-[#70BFE9]">
        Crear una cuenta para: Paciente
      </h2>

      <form v-if="step === 1" @submit.prevent="verifyLinkCode">
        <div class="flex flex-col items-center justify-center space-y-4">
          <p class="text-gray-600 dark:text-gray-300 text-center mb-4">
            Código de enlace proporcionado por tu profesional de la Salud Mental
          </p>
          <div class="relative w-full">
            <input
              v-model="linkCode"
              type="text"
              placeholder="Ingresa tu código..."
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLink
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
            />
          </div>
          <p v-if="error" class="text-sm text-red-500 mt-2">{{ error }}</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Siguiente
          </button>
        </div>
      </form>

      <form v-else-if="step === 2" @submit.prevent="submitPersonalData">
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <div class="relative">
                  <input
                    v-model="form.name"
                    @blur="validateName"
                    type="text"
                    placeholder="Ingresa tu(s) nombre(s)"
                    class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                    :class="{
                      'border-red-500 dark:border-red-500 focus:ring-red-500': nameError,
                      'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !nameError
                    }"
                    required
                  />
                  <IconUser
                    class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
                  />
              </div>
              <p v-if="nameError" class="text-sm text-red-500 mt-2">{{ nameError }}</p>
            </div>

            <div>
              <div class="relative">
                  <input
                    v-model="form.alias"
                    @blur="validateAlias"
                    type="text"
                    placeholder="Ingresa tu alias..."
                    class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                    :class="{
                      'border-red-500 dark:border-red-500 focus:ring-red-500': aliasError,
                      'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !aliasError
                    }"
                    required
                  />
                  <IconUserPlus
                    class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
                  />
              </div>
              <p v-if="aliasError" class="text-sm text-red-500 mt-2">{{ aliasError }}</p>
          </div>


          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <div class="relative">
                <input
                  v-model="form.paternalLastName"
                  @blur="validatePaternalLastName"
                  type="text"
                  placeholder="Ingresa tu primer apellido"
                  class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                  :class="{
                    'border-red-500 dark:border-red-500 focus:ring-red-500': paternalLastNameError,
                    'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !paternalLastNameError
                  }"
                  required
                  :style="{ 'padding-left': '3rem' }"
                />
                <IconUserCheck
                  class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
                />
              </div>
                <p v-if="paternalLastNameError" class="text-sm text-red-500 mt-2">{{ paternalLastNameError }}</p>
            </div>

            <div>
              <div class="relative">
                  <input
                    v-model="form.maternalLastName"
                      @blur="validateMaternalLastName"
                      type="text"
                      placeholder="Ingresa tu segundo apellido"
                      class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                      :class="{
                        'border-red-500 dark:border-red-500 focus:ring-red-500': maternalLastNameError,
                        'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !maternalLastNameError
                      }"
                    :style="{ 'padding-left': '3rem' }"
                  />
                  <IconUserCheck
                    class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
                  />
              </div>
              <p v-if="maternalLastNameError" class="text-sm text-red-500 mt-2">{{ maternalLastNameError }}</p>
          </div>
        </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
            <div class="relative">
              <input
                v-model="form.dateOfBirth"
                @change="validateDateOfBirth" type="date"
                class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                :class="{
                  'border-red-500 dark:border-red-500 focus:ring-red-500': dateOfBirthError,
                  'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !dateOfBirthError
                }"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconCalendar
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
              <p v-if="dateOfBirthError" class="text-sm text-red-500 mt-2">{{ dateOfBirthError }}</p>

            </div>

            <div>
            <div class="relative">
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#70BFE9]"
                required
                :style="{ 'padding-left': '3rem' }"
              >
                <option value="" disabled>Selecciona el género...</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
                <option value="non_binary">No binario</option>
                <option value="other">Otro</option>
              </select>
              <IconGenderBigender
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
            </div>
          </div>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Siguiente
          </button>
        </div>
      </form>

      <form v-else-if="step === 3" @submit.prevent="createAccount">
        <div class="space-y-4">
          <div>
            <div class="relative">
              <input
                v-model="form.email"
                type="email"
                placeholder="Ingresa tu correo electrónico"
                @blur="validateEmail" class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
                :class="{
                  'border-red-500 dark:border-red-500 focus:ring-red-500': emailError,
                  'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !emailError
                }"
                required
                :style="{ 'padding-left': '3rem' }"
              />
              <IconMail
                class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
              />
            </div>
            <p v-if="emailError" class="text-sm text-red-500 mt-2">{{ emailError }}</p>
          </div>

          <div>
          <div class="relative">
            <input
              v-model="form.password"
              type="password"
              placeholder="Ingresa tu contraseña"
              class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
              :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': passwordError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !passwordError
              }"
              required
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLock
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
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

          <div>
          <div class="relative">
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="Vuelve a introducir la contraseña"
              class="w-full pl-12 pr-4 py-3 rounded-lg border bg-gray-50 ..."
               :class="{
                'border-red-500 dark:border-red-500 focus:ring-red-500': passwordError,
                'border-gray-300 dark:border-gray-600 focus:ring-[#70BFE9]': !passwordError
              }"
              required
              :style="{ 'padding-left': '3rem' }"
            />
            <IconLock
              class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500"
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
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">* Campos obligatorios</p>
          <button
            type="submit"
            class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
            :disabled="loading"
          >
            Crear cuenta
          </button>
        </div>
      </form>

      <div v-else-if="step === 4" class="text-center">
        <div class="mb-6 flex flex-col items-center">
          <IconCircleCheckFilled class="text-green-500 w-20 h-20 mb-4" />
          <p class="text-lg font-medium text-gray-700 dark:text-gray-200">
            ¡Gracias por completar el registro!
          </p>
        </div>
        <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">
          Se te ha enviado un correo electrónico con un código de validación para confirmar tu
          cuenta.
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Revisa tu bandeja de entrada y, si no lo encuentras, revisa también la carpeta de spam.
        </p>
        <button
          @click="goToLogin"
          class="w-full mt-6 py-3 px-4 rounded-lg bg-[#70BFE9] text-white font-semibold hover:bg-[#5a9cbf] transition-colors duration-300"
        >
          Iniciar sesión
        </button>
      </div>
    </div>
  </BackgroundWrapper>
</template>

<script setup lang="ts">
import { ref, reactive, computed, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import { isAxiosError } from 'axios';
import BackgroundWrapper from '@/modules/auth/components/BackgroundWrapper.vue'
import * as AuthServices from '@/modules/auth/services/authServices';
import {
  IconLink,
  IconUser,
  IconUserPlus,
  IconUserCheck,
  IconCalendar,
  IconGenderBigender,
  IconMail,
  IconLock,
  IconCircleCheckFilled,
} from '@tabler/icons-vue'

const router = useRouter()

const step = ref(1)
const linkCode = ref('')
const professionalId = ref('')
const error = ref('')
const passwordError = ref('')
const loading = ref(false)
const linkCodeError = ref('') //Variable para errores del código de enlace

const nameError = ref('');
const aliasError = ref('');
const paternalLastNameError = ref('');
const maternalLastNameError = ref('');
const dateOfBirthError = ref('');
const genderError = ref('');
const emailError = ref('');

const hasAttemptedStep2 = ref(false);
const hasAttemptedStep3 = ref(false);

const form = reactive({
  name: '',
  alias: '',
  paternalLastName: '',
  maternalLastName: '',
  dateOfBirth: '',
  gender: '',
  email: '',
  password: '',
  confirmPassword: '',
})

async function verifyLinkCode() {
  loading.value = true
  linkCodeError.value = ''

  try {
    const response = await AuthServices.validateLinkCode(linkCode.value);

    if (response.status === 200) {
      professionalId.value = response.data.professional_id // Guardamos el ID del terapeuta
      step.value = 2 // Avanzar al paso de Datos Personales
    }
  } catch (err: unknown) {
    if (isAxiosError(err) && err.response && err.response.data.error) {
        linkCodeError.value = err.response.data.error;
        //Mostrar el error en la interfaz
        error.value = linkCodeError.value;
    } else {
        linkCodeError.value = 'El servidor no pudo verificar el código. Inténtalo de nuevo.';
    }
  } finally {
    loading.value = false
  }
}

// VALIDACIÓN DE CONTRASEÑA
const passwordRequirements = [
  { regex: /[a-z]/, text: 'Al menos una letra minúscula' },
  { regex: /[A-Z]/, text: 'Al menos una letra mayúscula' },
  // { regex: /\d/, text: 'Al menos un número' },
  { regex: /[@$!%*?&]/, text: 'Al menos un carácter especial (@$!%*?&)' },
  { regex: /.{8,32}/, text: 'Entre 8 y 32 caracteres' }
];
const passwordValidation = computed(() => {
  return passwordRequirements.map(req => ({
    ...req,
    met: req.regex.test(form.password)
  }));
});
const isPasswordValid = computed(() => passwordValidation.value.every(req => req.met));

// VALIDACIÓN DE CAMPOS DE TEXTO (Nombre, Apellidos, Alias)
const validateTextField = (fieldValue: string, errorRef: Ref<string>, fieldName: string) => {
  const textRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/;

  // 1. Validar formato (SIEMPRE, si hay texto)
  if (fieldValue.trim() && !textRegex.test(fieldValue)) {
    errorRef.value = `El ${fieldName} solo puede contener letras y espacios.`;
    return false;
  }

  // 2. Validar "obligatorio" (SOLO SI SE INTENTÓ ENVIAR)
  if (hasAttemptedStep2.value && !fieldValue.trim()) {
    errorRef.value = `El ${fieldName} es obligatorio.`;
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

  // 2. Si está vacío, está bien (es opcional)
  errorRef.value = '';
  return true; // Pasa
};

// VALIDACIÓN DE FECHA DE NACIMIENTO
const validateDateOfBirth = () => {
  // 1. Validar "obligatorio" (SOLO SI SE INTENTÓ ENVIAR)
  if (hasAttemptedStep2.value && !form.dateOfBirth) {
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

  if (birthDate > today) {
    dateOfBirthError.value = 'La fecha de nacimiento no puede ser en el futuro.';
    return false;
  }

  const age = today.getFullYear() - birthDate.getFullYear();
  const monthDifference = today.getMonth() - birthDate.getMonth();
  const dayDifference = today.getDate() - birthDate.getDate();

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
    return false;
  }

  dateOfBirthError.value = '';
  return true;
};

// VALIDACIÓN DE GÉNERO (que no esté vacío)
const validateGender = () => {
  // Validar "obligatorio" (SOLO SI SE INTENTÓ ENVIAR)
  if (hasAttemptedStep2.value && !form.gender) {
    genderError.value = 'Debes seleccionar un género.';
    return false;
  }
  genderError.value = '';
  return true;
};

// VALIDACIÓN DE CORREO
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Validar "obligatorio" (SOLO SI SE INTENTÓ ENVIAR - usa la bandera del paso 3)
  if (hasAttemptedStep3.value && !form.email) {
     emailError.value = 'El correo es obligatorio.';
     return false;
  }

  // Validar formato (SIEMPRE, si hay texto)
  if (form.email && !emailRegex.test(form.email)) {
    emailError.value = 'Formato de correo inválido (ej. nombre@dominio.com)';
    return false;
  }
  emailError.value = '';
  return true;
};

// --- WRAPPERS para llamar con @blur ---
const validateName = () => validateTextField(form.name, nameError, 'nombre');
const validateAlias = () => validateTextField(form.alias, aliasError, 'alias');
const validatePaternalLastName = () => validateTextField(form.paternalLastName, paternalLastNameError, 'primer apellido');
const validateMaternalLastName = () => validateOptionalTextField(form.maternalLastName, maternalLastNameError, 'segundo apellido');


function submitPersonalData() {
  hasAttemptedStep2.value = true; // Marca que se intentó enviar el paso 2
  const isNameValid = validateName();
  const isAliasValid = validateAlias();
  const isPaternalLastNameValid = validatePaternalLastName();
  const isMaternalLastNameValid = validateMaternalLastName();
  const isDateOfBirthValid = validateDateOfBirth();
  const isGenderValid = validateGender();

  if (
    isNameValid && isAliasValid && isPaternalLastNameValid &&
    isMaternalLastNameValid && isDateOfBirthValid && isGenderValid
  ) {
    // Si todo está bien, avanza al siguiente paso
    step.value = 3;
    error.value = ''; // Limpia el error general
  } else {
    // Si algo falla, muestra un error general
    error.value = 'Por favor, corrige los campos marcados en rojo.';
  }
}

async function createAccount() {
  hasAttemptedStep3.value = true; // Marca que se intentó enviar el paso 3
  // 1. Limpia errores y valida todo
  passwordError.value = '';
  const isEmailValid = validateEmail();

  if (form.password !== form.confirmPassword) {
    passwordError.value = 'Las contraseñas no coinciden.';
  }
  if (!isPasswordValid.value) {
    passwordError.value = (passwordError.value + ' La contraseña no cumple los requisitos.').trim();
  }

  // 2. Detener si hay CUALQUIER error
  if (!isEmailValid || passwordError.value) {
    return;
  }

  loading.value = true
  passwordError.value = ''

  try {
    // 1. Prepara el payload con la estructura anidada y la vinculación
    const registrationPayload = {
  // Los campos del 'user' ahora están en el nivel principal
  email: form.email,
  password: form.password,
  name: form.name,
  paternal_last_name: form.paternalLastName, // <-- Asegúrate que los nombres coincidan
  maternal_last_name: form.maternalLastName,
  date_of_birth: form.dateOfBirth,
  role: 'patient', // Rol fijo

  // Campos del modelo Patient
  alias: form.alias,
  gender: form.gender,
  professional_id: professionalId.value, // Este campo no lo usas en PreRegistration, pero no causa error
}

    // 2. Envía la solicitud al endpoint de registro
    const response = await AuthServices.registerPatient(registrationPayload);
    if (response.status === 201) {
        step.value = 4 // Mostrar el mensaje de éxito
    }

  } catch (err: unknown) {
    if (isAxiosError(err) && err.response && err.response.data) {

        let msg = 'Error de registro. Verifique su información.';
        const data = err.response.data;

        // Intentamos extraer el error del campo 'user' (que es el serializador anidado)
        if (data.user) {
            const userErrors = data.user;
            if (userErrors.email) msg = `Correo: ${userErrors.email[0]}`;
            else if (userErrors.date_of_birth) msg = `Fecha de Nacimiento: ${userErrors.date_of_birth[0]}`;
            else if (userErrors.password) msg = `Contraseña: ${userErrors.password[0]}`;
            else msg = 'Campos de usuario incompletos.';
        }
        // Si el error es del serializer Patient (ej. alias o gender)
        else if (data.alias) {
            msg = `Alias: ${data.alias[0]}`;
        }
        else if (data.professional_id) {
            msg = `Terapeuta: ${data.professional_id[0]}`;
        }
        else if (data.detail) {
             msg = data.detail; // Error genérico de DRF
        }

        passwordError.value = msg;

    } else {
        passwordError.value = 'Ocurrió un error en el servidor. Inténtalo de nuevo.'
    }
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push({
    name: 'first-login',
    params: { type: 'patient' }, // 1. Le pasamos el parámetro 'type'
    query: { email: form.email }    // 2. Le pasamos el email para que el formulario se auto-rellene
  });
}
</script>
