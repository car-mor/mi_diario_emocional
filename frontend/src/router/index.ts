import { createRouter, createWebHistory } from 'vue-router'
import WelcomeView from '../modules/auth/views/WelcomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: WelcomeView,
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
      path: '/login',
      name: 'login',
      component: () => import('../modules/auth/views/LoginView.vue'),
    },
    {
      path: '/home-patient',
      name: 'home-patient',
      component: () => import('../modules/patient/views/HomePatientView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/modules/auth/views/RegisterView.vue'),
    },
    {
      path: '/register-patient',
      name: 'register-patient',
      component: () => import('@/modules/auth/views/RegisterPatientView.vue'),
    },
    {
      path: '/register-professional',
      name: 'register-professional',
      component: () => import('@/modules/auth/views/RegisterProfessionalView.vue'),
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/modules/auth/views/ForgotPasswordView.vue'),
    },
    {
      path: '/profile-patient-mobile',
      name: 'profile-patient-mobile',
      component: () => import('@/modules/patient/views/PatientProfileMobileView.vue'),
    },
    {
      path: '/article-weekly-patient',
      name: 'article-weekly-patient',
      component: () => import('../modules/patient/views/ArticleWeekPatientView.vue'),
    },
    {
      path: '/video-carrusel-1-patient',
      name: 'video-carrusel-1-patient',
      component: () => import('../modules/patient/views/VideoCarrusel1PatientView.vue'),
    },
    {
      path: '/audiobook-carrusel-2-patient',
      name: 'audiobook-carrusel-2-patient',
      component: () => import('../modules/patient/views/AudiolibroCarrusel2PatientView.vue'),
    },
    {
      path: '/first-login',
      name: 'first-login',
      component: () => import('@/modules/auth/views/FirstLoginView.vue'),
    },
    {
      path: '/meditation-carrusel-3-patient',
      name: 'meditation-carrusel-3-patient',
      component: () => import('@/modules/patient/views/MeditationCarrusel3PatientView.vue'),
    },
    {
      path: '/video-carrusel-4-patient',
      name: 'video-carrusel-4-patient',
      component: () => import('@/modules/patient/views/VideoCarrusel4PatientView.vue'),
    },
    {
      path: '/conference-carrusel-5-patient',
      name: 'conference-carrusel-5-patient',
      component: () => import('@/modules/patient/views/ConferenceCarrusel5PatientView.vue'),
    },
    {
      path: '/faqs-patient',
      name: 'faqs-patient',
      component: () => import('@/modules/patient/views/FAQsPatientView.vue'),
    },
  ],
})

export default router
