<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 to-[#70BFE9]/20 dark:from-gray-900 dark:to-gray-800 transition-colors"
  >
    <div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
      <div class="min-h-screen flex items-center justify-center">
        <WomanHeart />
      </div>

      <div class="flex items-center justify-center p-6">
        <div
          class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-800 p-8 shadow-lg border border-gray-200 dark:border-gray-700"
        >
          <h1 class="mb-8 text-3xl font-bold text-center text-[#70BFE9]">Iniciar sesión</h1>

          <form @submit.prevent="login">
            <div class="mb-6">
              <label
                for="email"
                class="block text-gray-700 dark:text-gray-300 text-base font-semibold mb-2"
              >
                Correo electrónico
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <IconMail class="h-6 w-6 mx-auto text-[#70BFE9] dark:text-gray-300" />
                </div>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  placeholder="Ingresa tu correo electrónico"
                  class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
                  required
                />
              </div>
            </div>

            <div class="mb-6">
              <label
                for="password"
                class="block text-gray-700 dark:text-gray-300 text-base font-semibold mb-2"
              >
                Contraseña
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <IconLockSquareRounded
                    class="h-6 w-6 mx-auto text-[#70BFE9] dark:text-gray-300"
                  />
                </div>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  placeholder="Ingresa tu contraseña"
                  class="pl-10 p-3 w-full border rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              class="w-full bg-[#70BFE9] hover:bg-[#3457B2] text-white font-semibold py-3 px-6 rounded-lg transition-colors mb-4"
            >
              Iniciar sesión
            </button>
            <router-link
              to="/"
              class="w-full inline-block text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Regresar al Inicio
            </router-link>
          </form>

          <div class="mt-8 text-center text-gray-600 dark:text-gray-400">
            ¿No tienes una cuenta?
            <router-link to="/register" class="text-[#70BFE9] hover:underline font-semibold ml-1">
              Regístrate aquí
            </router-link>
            <br />
            <router-link
              to="/forgot-password"
              class="text-[#70BFE9] hover:underline mt-2 inline-block"
            >
              Olvidé mi contraseña
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { IconLockSquareRounded, IconMail } from '@tabler/icons-vue'
import WomanHeart from '../components/WomanHeart.vue'

const email = ref('')
const password = ref('')

const login = () => {
  // Aquí iría tu lógica de autenticación
  console.log('Intento de inicio de sesión con:', email.value, password.value)
  // Por ejemplo, enviar a una API
  // fetch('/api/login', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ email: email.value, password: password.value })
  // })
  // .then(response => response.json())
  // .then(data => {
  //   if (data.success) {
  //     router.push('/dashboard'); // Redirige al usuario
  //   } else {
  //     alert(data.message);
  //   }
  // });
}
</script>
