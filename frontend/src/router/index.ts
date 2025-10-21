import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
    // Rutas Públicas de Bienvenida y Auth
    { path: '/', name: 'welcome', component: () => import('../modules/auth/views/WelcomeView.vue') },
    { path: '/login', name: 'login', component: () => import('../modules/auth/views/LoginView.vue') },
        {
      path: '/first-login/:type',
      name: 'first-login',
      component: () => import('@/modules/auth/views/FirstLoginView.vue'),
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/link-professional',
      name: 'link-professional',
      component: () => import('@/modules/auth/views/LinkProfessionalView.vue'),
      meta: { requiresAuth: true, role: 'patient' }
    },
  {
    path: '/not-approved-professional',
    name: 'not-approved-professional',
    component: () => import('@/modules/auth/views/NotApprovedProfessionalView.vue'),
    meta: { requiresAuth: true, role: 'professional' }, // Ruta protegida
  },
    {
      path: '/faq',
      name: 'faq',
      component: () => import('../modules/auth/views/FAQView.vue'),
    },
    {
      path: '/who-are-we',
      name: 'who-are-we',
      component: () => import('../modules/auth/views/WhoAreWeView.vue'),
    },
    {
      path: '/data-protection',
      name: 'data-protection',
      component: () => import('../modules/auth/views/DataProtectionView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/modules/auth/views/RegisterView.vue'),
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/modules/auth/views/ForgotPasswordView.vue'),
    },
        {
      path: '/register-patient',
      name: 'register-patient',
      component: () => import('@/modules/auth/views/RegisterPatientView.vue'),
// Ruta pública
    },
        {
      path: '/register-professional',
      name: 'register-professional',
      component: () => import('@/modules/auth/views/RegisterProfessionalView.vue'),
      meta: { requiresAuth: false, requiredRole: 'professional' } // Ruta pública
    },

    // Rutas Protegidas (requieren autenticación y rol específico)
    // Rutas de paciente
    {
      path: '/patient-layout',
      name: 'patient-layout',
      component: () => import('../modules/patient/views/PatientLayout.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' }, // METADATOS DE PROTECCIÓN
      children: [

        {
        path: '/home-patient',
        name: 'home-patient',
        component: () => import('../modules/patient/views/HomePatientView.vue'),
        meta: { requiresAuth: true, requiredRole: 'patient' } // METADATOS DE PROTECCIÓN
    },
    {
      path: '/profile-patient-mobile',
      name: 'profile-patient-mobile',
      component: () => import('@/modules/patient/views/PatientProfileMobileView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/article-weekly-patient',
      name: 'article-weekly-patient',
      component: () => import('../modules/patient/views/ArticleWeekPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/video-carrusel-1-patient',
      name: 'video-carrusel-1-patient',
      component: () => import('../modules/patient/views/VideoCarrusel1PatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
     {
      path: '/audiobook-carrusel-2-patient',
      name: 'audiobook-carrusel-2-patient',
      component: () => import('../modules/patient/views/AudiolibroCarrusel2PatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/meditation-carrusel-3-patient',
      name: 'meditation-carrusel-3-patient',
      component: () => import('@/modules/patient/views/MeditationCarrusel3PatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/video-carrusel-4-patient',
      name: 'video-carrusel-4-patient',
      component: () => import('@/modules/patient/views/VideoCarrusel4PatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/conference-carrusel-5-patient',
      name: 'conference-carrusel-5-patient',
      component: () => import('@/modules/patient/views/ConferenceCarrusel5PatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/word-cloud-patient',
      name: 'word-cloud-patient',
      component: () => import('@/modules/patient/views/WordCloudPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/faqs-patient',
      name: 'faqs-patient',
      component: () => import('@/modules/patient/views/FAQsPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/diary-history',
      name: 'diary-history',
      component: () => import('@/modules/patient/views/DiaryHistoryPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/pie-chart-patient',
      name: 'pie-chart-patient',
      component: () => import('@/modules/patient/views/PieChartPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/account-settings',
      name: 'account-settings',
      component: () => import('@/modules/patient/views/AccountSettingsPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },

    {
      path: '/unlinked-view',
      name: 'unlinked-view',
      component: () => import('@/modules/patient/views/UnlinkedView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
    {
      path: '/diary-register',
      name: 'diary-register',
      component: () => import('@/modules/patient/views/DiaryRegisterPatientView.vue'),
      meta: { requiresAuth: true, requiredRole: 'patient' } // Ruta protegida
    },
      ]
    },


    // Rutas de profesional

     {
      path: '/professional-layout',
      name: 'professional-layout',
      component: () => import('../modules/professional/views/ProfessionalLayout.vue'),
      meta: { requiresAuth: true, requiredRole: 'professional' }, // METADATOS DE PROTECCIÓN
      children: [
        {
            path: '', // Se activa cuando visitas /professional-layout
            name: 'home-professional',
            // Asegúrate de que la ruta al componente sea la correcta
            component: () => import('@/modules/professional/components/ProfessionalHome.vue'),
            meta: { requiresAuth: true, requiredRole: 'professional' }
        },
    {
        path: '/patient-management',
        name: 'patient-management',
        component: () => import('@/modules/professional/views/ManagementProfessionalView.vue'),
        meta: { requiresAuth: true, requiredRole: 'professional' } // METADATOS DE PROTECCIÓN
    },
    {
      path: '/videos-tutorials-professional',
      name: 'videos-tutorials-professional',
      component: () => import('../modules/professional/views/VideoTutorialsProfessionalView.vue'),
      meta: { requiresAuth: true, requiredRole: 'professional' } // Ruta protegida
    },
    {
      path: '/faqs-tutorials-professional',
      name: 'faqs-tutorials-professional',
      component: () => import('../modules/professional/views/FAQsProfessionalView.vue'),
      meta: { requiresAuth: true, requiredRole: 'professional' } // Ruta protegida
    },
    {
      path: '/patient-details/:id',
      name: 'patient-details',
      component: () => import('../modules/professional/views/PatientDetailsProfessionalView.vue'),
      meta: { requiresAuth: true, requiredRole: 'professional' } // Ruta protegida
    },
  ]
}    ,
 {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/modules/auth/views/NotFoundView.vue'),
    } ];


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// --- GUARDIA DE NAVEGACIÓN GLOBAL ---
router.beforeEach(async (to, from, next) => { // <-- Hacemos la función 'async'
  const authStore = useAuthStore();

  // Es buena práctica esperar a que el estado inicial de auth se resuelva
  if (!authStore.isAuthReady) {
    await authStore.checkInitialAuth();
  }
  const isAuthenticated = !!authStore.authToken;
  const userRole = authStore.userType;
  const reviewStatus = authStore.reviewStatus;
  const isPatientLinked = authStore.isLinked;

  // Regla 1: Paciente no vinculado intenta acceder a rutas restringidas
  // Si es un paciente autenticado, pero no está vinculado...
  if (userRole === 'patient' && isAuthenticated && !isPatientLinked) {
    // Y NO está intentando ir a la página de vinculación...
    if (to.name !== 'link-professional') {
      // Lo redirigimos forzosamente a la página de vinculación.
      return next({ name: 'link-professional' });
    }
  }

  // --- NUEVA REGLA PARA EVITAR QUE UN PACIENTE VINCULADO VEA LA PÁGINA DE VINCULACIÓN ---
  if (userRole === 'patient' && isAuthenticated && isPatientLinked && to.name === 'link-professional') {
    // Si ya está vinculado, lo mandamos a su página de inicio.
    return next({ name: 'home-patient' });
  }

  // Regla 2: Si la ruta es protegida y no está autenticado -> a login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login' });
  }

  // Regla 3: Si está autenticado y va a una ruta pública -> a su dashboard
  // Añadimos una excepción para que puedan ir a /logout
  if (to.name && ['login', 'register', 'welcome'].includes(to.name as string) && isAuthenticated) {
    if (userRole === 'patient') return next({ name: 'home-patient' });
    if (userRole === 'professional') {
      return reviewStatus === 'APPROVED' ? next({ name: 'professional-layout' }) : next({ name: 'not-approved-professional' });
    }
  }

  // Regla 4: Si está autenticado y va a una ruta protegida -> verificar permisos
 if (to.meta.requiresAuth && isAuthenticated) {
    const requiredRole = to.meta.requiredRole as string;

    // Comprobamos si la ruta requiere un rol y si el usuario no lo cumple
    if (requiredRole && userRole !== requiredRole) {
      // Redirige a una página de "no autorizado" o a la de bienvenida
      return next({ name: 'welcome' });
    }
  }



  // Si no se cumple ninguna regla de redirección, continuar.
  next();
});
export default router
