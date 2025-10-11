import { ref } from 'vue';
import { defineStore } from 'pinia';
import {
  type BaseCredentials,
  type UserProfileData,
  login as apiLogin,
  logoutBlacklist,
  fetchUserProfile as apiFetchProfile
} from '@/modules/auth/services/authServices';

export type UserType = 'patient' | 'professional' | 'anonymous' | 'superuser' | null;

export const useAuthStore = defineStore('auth', () => {
  const authToken = ref<string | null>(localStorage.getItem('authToken'));
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'));
  const userType = ref<UserType>((localStorage.getItem('userType') as UserType) || 'anonymous');
  const reviewStatus = ref<string | null>(localStorage.getItem('reviewStatus'));
  const loading = ref(false);
  const isAuthReady = ref(false);
  const userProfile = ref<UserProfileData | null>(null);

  const setTokens = (access: string, refresh: string) => {
    authToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem('authToken', access);
    localStorage.setItem('refreshToken', refresh);
  };

  const setUserData = (role: UserType, status: string | null = null) => {
    userType.value = role;
    localStorage.setItem('userType', role || 'anonymous');
    if (status) {
      reviewStatus.value = status;
      localStorage.setItem('reviewStatus', status);
    } else {
      reviewStatus.value = null;
      localStorage.removeItem('reviewStatus');
    }
  };

  const fetchUserProfile = async () => {
    if (!authToken.value) return;
    try {
      const response = await apiFetchProfile();
      userProfile.value = response.data;
    } catch (error) {
      console.error("Error al obtener el perfil del usuario:", error);
    }
  };

  const login = async (credentials: BaseCredentials): Promise<string> => {
    loading.value = true;
    try {
      const response = await apiLogin(credentials);
      const { access, refresh, role, review_status } = response.data;
      setTokens(access, refresh);
      setUserData(role, review_status);
      await fetchUserProfile();

      if (role === 'patient') return '/patient-layout';
      if (role === 'professional') {
        return review_status === 'APPROVED' ? '/professional-layout' : '/pending-approval';
      }
      return '/login';
    } catch (error: unknown) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    const currentRefreshToken = refreshToken.value;
    userProfile.value = null;
    userType.value = 'anonymous';
    authToken.value = null;
    refreshToken.value = null;
    reviewStatus.value = null;
    localStorage.clear();

    if (currentRefreshToken) {
      try {
        await logoutBlacklist(currentRefreshToken);
      } catch (e) {
        console.warn("Error al invalidar el token en el servidor.", e);
      }
    }
    window.location.href = '/login';
  };

  const checkInitialAuth = async () => {
    if (authToken.value) {
      await fetchUserProfile();
    }
    isAuthReady.value = true;
  }

  return {
    userType,
    authToken,
    refreshToken,
    loading,
    isAuthReady,
    login,
    logout,
    setTokens,
    setUserData,
    userProfile,
    fetchUserProfile,
    checkInitialAuth,
    reviewStatus // <-- ¡AÑADIDO AQUÍ!
  };
});

