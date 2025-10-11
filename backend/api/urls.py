# api/urls.py (Versión Corregida y Limpia)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

# --- CORRECCIÓN EN IMPORTS ---
# 1. Importa SÓLO las vistas genéricas que necesitas de simplejwt
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

# 3. Importa el resto de tus vistas y viewsets como ya lo haces
from diary.views import DiaryEntryViewSet
from reports.views import WeeklyReportViewSet

# 2. Importa TU vista de login personalizada desde la app 'users'
from users.views import (
    MyTokenObtainPairView,
    PasswordResetConfirmView,
    PatientRegistrationView,
    ProfessionalRegistrationView,
    RegenerateLinkCodeView,
    RequestPasswordResetView,
    ResendVerificationCodeView,
    UserProfileView,
    ValidateLinkCodeView,
    VerifyEmailView,
    VerifyProfessionalEmailView,
)

# El resto del archivo se queda exactamente igual
# -----------------------------------------------

# Paso 1: Inicializar el Router
router = DefaultRouter()

# Paso 2: Registrar todos los ViewSets en el Router
router.register("diary-entries", DiaryEntryViewSet, basename="diary-entry")
router.register("weekly-reports", WeeklyReportViewSet, basename="weekly-report")


# Paso 3: Definir urlpatterns
urlpatterns = [
    path("register/patient/", PatientRegistrationView.as_view(), name="register-patient"),
    path("register/professional/", ProfessionalRegistrationView.as_view(), name="register-professional"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("verify-professional-email/", VerifyProfessionalEmailView.as_view(), name="verify-professional-email"),
    path("password-reset/", RequestPasswordResetView.as_view(), name="request-password-reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("resend-verification/", ResendVerificationCodeView.as_view(), name="resend-verification"),
    path("profile/me/", UserProfileView.as_view(), name="user-profile-me"),
    path("profile/regenerate-link/", RegenerateLinkCodeView.as_view(), name="regenerate-link"),
    path("validate-link/", ValidateLinkCodeView.as_view(), name="validate-link"),
    # Esta sección ahora es clara y sin ambigüedades
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("", include(router.urls)),
]
