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
        // Aquí puedes definir rutas hijas si es necesario
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
      path: '/patient-management',
      name: 'patient-management',
      component: () => import('@/modules/professional/views/ManagementProfessionalView.vue'),
      meta: { requiresAuth: true, requiredRole: 'professional' } // Ruta protegida
    },
    {
      path: '/patient-details',
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
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.authToken;
  const userRole = authStore.userType;
  const reviewStatus = authStore.reviewStatus;

  // Regla 1: Si la ruta es protegida y no está autenticado -> a login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login' });
  }

  // Regla 2: Si está autenticado y va a una ruta pública -> a su dashboard
  if (!to.meta.requiresAuth && isAuthenticated) {
    if (userRole === 'patient') return next({ name: 'patient-layout' });
    if (userRole === 'professional') {
      return reviewStatus === 'APPROVED' ? next({ name: 'professional-layout' }) : next({ name: 'not-approved-professional' });
    }
  }

  // Regla 3: Si está autenticado y va a una ruta protegida -> verificar permisos
  if (to.meta.requiresAuth && isAuthenticated) {
    const requiredRole = to.meta.role as string;
    const requiredStatus = to.meta.status as string;

    if (requiredRole && userRole !== requiredRole) {
      return next({ name: 'welcome' }); // Rol incorrecto, fuera
    }

    // Profesional no aprobado intenta acceder a su dashboard
    if (userRole === 'professional' && requiredStatus && reviewStatus !== requiredStatus) {
      return next({ name: 'not-approved-professional' }); // Forzar a la pantalla de espera
    }
  }

  // Si todo está bien, continuar
  next();
});
export default router
