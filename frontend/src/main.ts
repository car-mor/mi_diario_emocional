import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'
import './styles/index.css'
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

const app = createApp(App)
app.use(createPinia())

// --- NUEVO FLUJO DE INICIALIZACIÓN (MÁS SIMPLE Y SEGURO) ---

// 1. Inicializamos la tienda de Pinia
const authStore = useAuthStore();

// 2. Esperamos explícitamente a que la verificación inicial termine.
//    Esto pausa el montaje de la app hasta que sepamos si el usuario está logueado
//    y tengamos sus datos de perfil.
await authStore.checkInitialAuth();

// ----------------------------------------------------------------

// 3. Una vez que la verificación termina, continuamos con el montaje de la app.
app.use(router)
app.mount('#app')
