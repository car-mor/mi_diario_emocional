import { defineStore } from 'pinia'
import { ref, watchEffect } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Inicializar con el tema guardado o preferencia del sistema
  const getInitialTheme = () => {
    // Primero revisa si hay tema guardado
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      return savedTheme === 'dark'
    }
    // Si no, usa la preferencia del sistema
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  const isDark = ref(getInitialTheme())

  const toggleDark = () => {
    isDark.value = !isDark.value
  }

  // Aplicar tema al HTML y guardarlo
  watchEffect(() => {
    const html = document.documentElement

    if (isDark.value) {
      html.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      html.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  })

  return { isDark, toggleDark }
})
