// src/modules/auth/services/authServices.ts
import axios, { type AxiosResponse, type AxiosError} from 'axios'; // <-- CORRECCIÓN 1: 'type' keyword for AxiosResponse
import { useAuthStore } from '@/store/auth';

// ----------------------------------------------------------------------
// TIPOS DE DATOS (Payloads)
// ----------------------------------------------------------------------

// Tipo base para las credenciales de login/registro

export interface BaseCredentials {
  email: string;
  password: string;
}


interface UserRegistrationFields extends BaseCredentials {
  name: string;
  paternal_last_name: string;
  maternal_last_name: string;
  date_of_birth: string;
  role: string;
}


// Tipo para el payload completo de registro de paciente
interface PatientRegistrationPayload extends UserRegistrationFields {
  // Hereda email, password, name, paternal_last_name, etc.

  // Y le añadimos los campos específicos del perfil de paciente
  alias: string;
  gender: string;
  professional_id: string;
}

// Tipo COMPLETO para el registro de profesional
interface ProfessionalRegistrationPayload  {
  // Campos del modelo User (requeridos para la creación)
 user: UserRegistrationFields;

  // Campos del perfil de Professional
  professional_license: string;
  curp: string;
  sex: string;
  career: string;
  institution: string;
  link_code?: string;
}

// Tipo para el payload de verificación de correo
interface VerificationPayload {
  email: string;
  verification_code: string;
}

// Tipo para el payload de restablecimiento de contraseña
interface PasswordResetConfirmPayload {
    code: string; // ANTES: token
    new_password: string;
    confirm_password: string;
}

export interface PatientAliasUpdatePayload {
    alias: string;
}

export interface ChangePasswordPayload {
    current_password: string;
    new_password: string;
    new_password_confirm: string;
}

export interface RequestEmailChangePayload {
    current_password: string;
    new_email: string;
}

export interface ConfirmEmailChangePayload {
    new_email: string;
    verification_code: string;
}

export interface DeleteAccountPayload {
    password: string;
}

interface ActivationPayload {
  email: string;
  password: string; // La contraseña ahora es necesaria
  verification_code: string;
}

// ----------------------------------------------------------------------
// FUNCIONES DEL SERVICIO (Rutas de la API)
// ----------------------------------------------------------------------
export const activateAccount = async (data: ActivationPayload): Promise<AxiosResponse> => {
  // Apunta a tu endpoint que ahora lo hace todo
  return api.post('verify-email/', data);
};

export const verifyProfessionalEmail = async (data: ActivationPayload): Promise<AxiosResponse> => {
  return api.post('verify-professional-email/', data);
};

export const changePassword = async (data: ChangePasswordPayload): Promise<AxiosResponse> => {
    return api.post('profile/change-password/', data);
};

export const requestEmailChange = async (data: RequestEmailChangePayload): Promise<AxiosResponse> => {
    return api.post('profile/request-email-change/', data);
};

export const confirmEmailChange = async (data: ConfirmEmailChangePayload): Promise<AxiosResponse> => {
    return api.post('profile/confirm-email-change/', data);
};

export const deleteAccount = async (data: DeleteAccountPayload): Promise<AxiosResponse> => {
    return api.post('profile/delete-account/', data);
};

export const registerPatient = async (data: PatientRegistrationPayload): Promise<AxiosResponse> => {
  return api.post('register/patient/', data);
};

export const registerProfessional = async (data: ProfessionalRegistrationPayload): Promise<AxiosResponse> => { // <-- FIX APLICADO
  return api.post('register/professional/', data);
};

export const verifyEmail = async (data: VerificationPayload): Promise<AxiosResponse> => {
  return api.post('verify-email/', data);
};

export const login = async (data: BaseCredentials): Promise<AxiosResponse> => {
  return api.post('token/', data);
};

export const refreshToken = async (data: { refresh: string }): Promise<AxiosResponse> => {
  return api.post('token/refresh/', data);
};

export const requestPasswordReset = async (data: { email: string }): Promise<AxiosResponse> => {
  return api.post('password-reset/', data);
};

export const verifyPasswordResetCode = async (data: { code: string }): Promise<AxiosResponse> => {
    return api.post('password-reset/verify/', data);
};

export const passwordResetConfirm = async (data: PasswordResetConfirmPayload): Promise<AxiosResponse> => {
    return api.post('password-reset/confirm/', data);
};

export const resendVerificationCode = async (data: { email: string, password: string }): Promise<AxiosResponse> => {
    return api.post('resend-verification/', data);
};

export const updatePatientAlias = async (data: PatientAliasUpdatePayload): Promise<AxiosResponse> => {
    // Usamos el mismo endpoint 'profile/me/' con el método PATCH
    return api.patch('profile/me/', data);
};

export interface ProfessionalProfile {
    name: string;
    paternal_last_name: string;
    maternal_last_name: string;
    email: string;
    sex: string;
    link_code: string;
    // Añade el resto de campos que quieras mostrar
}
// Interfaz para actualizar los datos editables del paciente
export interface PatientUpdatePayload {
    description?: string; // Hacemos la descripción OPCIONAL para el PATCH
    profile_picture?: string | null; // La URL de la foto de perfil (o null para eliminarla)
}

export const updatePatientProfile = async (data: PatientUpdatePayload | FormData): Promise<AxiosResponse> => {
    // Si es FormData, no interferir con el Content-Type (Axios lo maneja automáticamente)
    if (data instanceof FormData) {
        // NO establecer Content-Type manualmente, dejar que Axios lo haga
        return api.patch('profile/me/', data);
    }

    // Si es JSON (objeto), usar la configuración normal
    return api.patch('profile/me/', data);
};

export interface PatientProfile {
    name: string;
    paternal_last_name: string;
    maternal_last_name: string;
    description: string;
    email: string;
    alias: string;
    gender: string;
    profile_picture_url: string | null; // <-- URL de la foto o null/default
    professional_name?: string;
    is_linked: boolean;
    current_streak: number;
}

export type UserProfileData = ProfessionalProfile | PatientProfile

export const logoutBlacklist = async (refreshToken: string): Promise<AxiosResponse> => {
    // Esta petición NO lleva el access token en el header, solo el refresh token en el body.
    return axios.post(`${API_URL}logout/`, { refresh: refreshToken });
};

export const resendActivationCode = async (data: { email: string, role: string, password?: string }): Promise<AxiosResponse> => {
  // Apunta a la URL que configuraste en urls.py
  return api.post('resend-verification/', data);
};

export const regenerateLinkCode = async (): Promise<AxiosResponse<{ new_link_code: string }>> => {
    // Es una petición POST simple que no necesita cuerpo (el token identifica al usuario)
    return api.post('profile/regenerate-link/');
};

export const validateLinkCode = async (link_code: string): Promise<AxiosResponse<{ professional_id: string, message: string }>> => {
    return api.post('validate-link/', { link_code: link_code });
};

export const fetchUserProfile = async (): Promise<AxiosResponse<UserProfileData>> => {
    // La función ahora promete devolver PatientProfile O ProfessionalProfile
    return api.get('profile/me/');
};

export const uploadAvatar = async (file: File): Promise<AxiosResponse> => {
    const formData = new FormData();
    formData.append('profile_picture', file); // Asegúrate que 'profile_picture' sea el nombre de campo correcto

    return api.patch('profile/me/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data', // Sobrescribir el content-type para el archivo
        },
    });
};

// ----------------------------------------------------------------------
// CONFIGURACIÓN DE AXIOS E INTERCEPTOR
// ----------------------------------------------------------------------

const API_URL = import.meta.env.VITE_API_BASE_URL + '/api/';

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.authToken;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // ✅ Solo establecer JSON si NO es FormData
    if (!(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json';
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);



// Estas variables deben estar definidas fuera del interceptor para mantener su estado entre llamadas.
let isRefreshing = false;
let failedQueue: Array<{ resolve: (token: string) => void, reject: (error: AxiosError) => void }> = [];

// Esta función procesará la cola de peticiones pendientes una vez que el token se haya refrescado.
const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token as string);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const authStore = useAuthStore();
    const originalRequest = error.config;
    const status = error.response?.status;

    // Ignoramos los errores 401 que vienen de la propia página de login.
    const isLoginAttempt = originalRequest?.url === 'token/';

    if (status === 401 && originalRequest && !isLoginAttempt) {

      // Prevenimos bucles infinitos si la llamada para refrescar el token también falla.
      if (originalRequest.url === 'token/refresh/') {
          authStore.logout();
          return Promise.reject(error);
      }

      // Si no hay refresh token, no podemos hacer nada.
      if (!authStore.refreshToken) {
        authStore.logout();
        return Promise.reject(error);
      }

      // --- LÓGICA PARA ENCOLAR PETICIONES ---
      // Si ya hay un refresco en curso, encolamos la nueva petición.
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          // Cuando la promesa se resuelva, reintentamos la petición original con el nuevo token.
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${token}`;
          }
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }
      // --- FIN DE LA LÓGICA PARA ENCOLAR ---

      isRefreshing = true;

      try {
        // Intentamos obtener un nuevo access token.
        const response = await api.post('token/refresh/', { refresh: authStore.refreshToken });
        const newToken = response.data.access;

        // Actualizamos los tokens en Pinia.
        // Asumimos que el refresh token puede cambiar, como lo indica tu código anterior.
        authStore.setTokens(newToken, response.data.refresh || authStore.refreshToken);

        // Actualizamos el header de la petición original.
        if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
        }

        // Procesamos la cola de peticiones con el nuevo token.
        processQueue(null, newToken);

        // Reintentamos la petición original.
        return api(originalRequest);

      } catch (refreshError) {
        // Si el refresco falla, rechazamos todas las peticiones en cola y forzamos el logout.
        processQueue(refreshError as AxiosError, null);
        authStore.logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Devolvemos cualquier otro error para que sea manejado por el componente que hizo la llamada.
    return Promise.reject(error);
  }
);
