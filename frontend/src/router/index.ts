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
  ],
})

export default router
