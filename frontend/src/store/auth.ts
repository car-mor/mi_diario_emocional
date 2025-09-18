// src/stores/auth.ts
import { ref } from 'vue'
import { defineStore } from 'pinia'

// Define los tipos de usuario posibles, incluyendo 'anónimo'
export type UserType = 'paciente' | 'terapeuta' | 'anónimo'

export const useAuthStore = defineStore('auth', () => {
  // El estado inicial del usuario es 'anónimo'
  const userType = ref<UserType>('anónimo')

  const loginAs = (type: UserType) => {
    userType.value = type
  }

  const logout = () => {
    userType.value = 'anónimo'
  }

  return { userType, loginAs, logout }
})
