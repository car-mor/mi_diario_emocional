# importacion de secrets
import secrets
import uuid
from datetime import timedelta

from django.conf import settings  # Para acceder a variables de configuración
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import exceptions, generics, status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

# Importa los permisos (esto es clave para proteger tus vistas)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import EmailChangeRequest, PasswordReset, Patient, PreRegistration, Professional, User

# Importa los serializadores y modelos
from .serializers import (
    ChangePasswordSerializer,
    ConfirmEmailChangeSerializer,
    CustomTokenObtainPairSerializer,
    DeleteAccountSerializer,
    PatientProfileSerializer,
    PatientProfileUpdateSerializer,
    PatientSerializer,
    PreRegistrationSerializer,
    ProfessionalProfileSerializer,
    ProfessionalSerializer,
    RequestEmailChangeSerializer,
)
from .services import send_password_reset_email, send_verification_change_email, send_verification_email

# Importa tus funciones de servicio para correos, etc. (simuladas aquí)
# from .services import send_verification_email, send_password_reset_email


# Vista para el registro de pacientes
class PatientRegistrationView(APIView):
    """
    Gestiona el pre-registro de un paciente.
    No crea un usuario final, sino una entrada temporal que debe ser verificada.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PreRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            pre_registration = serializer.save()

            # --- Lógica para enviar el correo de verificación (ACTIVADA) ---
            send_verification_email(pre_registration.email, pre_registration.verification_code)
            # --------------------------------------------------------------

            return Response(
                {
                    "message": "Registro casi completo. Se ha enviado un código de verificación a tu correo.",
                    "email": pre_registration.email,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            print("SERIALIZER ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para el registro de profesionales
class ProfessionalRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProfessionalSerializer(data=request.data)
        if serializer.is_valid():
            # La creación del usuario y el perfil se manejan en el serializador
            # 1. El serializador ejecuta serializer.create(), que se encarga de:
            #    a) Crear el User (con password hasheada y is_active=False).
            #    b) Generar el verification_code y guardarlo.
            #    c) Enviar el correo electrónico con el código.
            #    d) Crear el perfil Professional.
            serializer.save()

            return Response(
                {"message": "Registro exitoso. Tu cuenta está en revisión y te notificaremos cuando sea aprobada."},
                status=status.HTTP_201_CREATED,
            )
        else:
            print("Errores del serializador:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para la verificación de correo electrónico (para ambos roles)
class VerifyEmailView(APIView):
    """
    Gestiona la activación final de la cuenta.
    Verifica el email, el código Y la contraseña.
    Si todo es correcto, crea el usuario final y devuelve los tokens de login.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Obtenemos los 3 datos clave del frontend
        email = request.data.get("email")
        password = request.data.get("password")
        verification_code = request.data.get("verification_code")

        if not all([email, password, verification_code]):
            return Response(
                {"error": "Email, contraseña y código de verificación son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 2. Buscamos en la tabla temporal PreRegistration
            prereg = PreRegistration.objects.get(email=email)

            # 3. Verificamos que el código no haya expirado
            if prereg.is_code_expired():
                return Response(
                    {"error": "El código de verificación ha expirado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 4. Verificamos que la contraseña y el código coincidan
            password_matches = check_password(password, prereg.hashed_password)
            code_matches = prereg.verification_code == verification_code

            if not password_matches or not code_matches:
                # Damos un error genérico para no revelar si falló el código o la contraseña
                return Response(
                    {"error": "El código de validación o las credenciales son incorrectas."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 5. ¡ÉXITO! Creamos el usuario y perfil en una transacción segura
            with transaction.atomic():
                # Creamos el usuario final
                user = User.objects.create_user(
                    email=prereg.email,
                    password=password,
                    is_active=True,
                    role=prereg.role,
                    **prereg.user_data,  # <-- CORRECCIÓN: Sin coma al final
                )

                # Creamos el perfil de paciente asociado
                if prereg.role == "patient":
                    profile_data = prereg.profile_data
                    professional_id = profile_data.pop("professional_id", None)  # Extraemos el ID

                    professional_instance = None
                    if professional_id:
                        try:
                            # Buscamos la instancia del Profesional
                            professional_instance = Professional.objects.get(pk=professional_id)
                        except Professional.DoesNotExist:
                            # Manejar el caso de que el profesional haya sido eliminado
                            # mientras el registro estaba pendiente.
                            pass

                    Patient.objects.create(
                        user=user,
                        professional=professional_instance,  # Asignamos la instancia
                        **profile_data,  # Pasamos el resto de los datos (alias, gender)
                    )
                # (Aquí podrías añadir la lógica para crear un 'professional' si es necesario)

                # 6. Limpiamos la tabla de pre-registro
                prereg.delete()

            # 7. Generamos y devolvemos los tokens JWT para el auto-login
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "¡Cuenta activada exitosamente! Has iniciado sesión.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {"email": user.email, "role": user.role},
                },
                status=status.HTTP_200_OK,
            )

        except PreRegistration.DoesNotExist:
            return Response(
                {"error": "No se encontró un registro pendiente para este correo."},
                status=status.HTTP_404_NOT_FOUND,
            )


class VerifyProfessionalEmailView(APIView):
    """Activa la cuenta de un Profesional que ya existe pero está inactivo."""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        verification_code = request.data.get("verification_code")

        try:
            user = User.objects.get(email=email, role="professional", is_active=False)

            if (
                not user.check_password(password)
                or user.verification_code != verification_code
                or user.verification_code_expires_at < timezone.now()
            ):
                raise User.DoesNotExist

            user.is_active = True
            user.verification_code = None
            user.verification_code_expires_at = None
            user.save()

            return Response(
                {"message": "Correo de profesional verificado con éxito. Ya puedes iniciar sesión."},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Credenciales o código incorrectos para una cuenta pendiente de activación."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Vista para solicitar recuperación de contraseña
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            PasswordReset.objects.filter(user=user).delete()

            # El modelo 'PasswordReset' usa un token UUID, pero para el usuario es más fácil un código corto.
            # Usaremos el UUID como 'token' interno y le enviaremos un código corto derivado de él.
            reset_instance = PasswordReset.objects.create(user=user, expires_at=timezone.now() + timedelta(minutes=5))

            # Generamos un código corto para el usuario a partir del token UUID
            user_friendly_code = str(reset_instance.token)[:6].upper()

            # Enviar el correo con el código corto
            send_password_reset_email(user.email, user_friendly_code)  # <-- LLAMA A LA NUEVA FUNCIÓN

            return Response(
                {"message": "Se ha enviado un código de recuperación a tu correo electrónico."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "El correo electrónico no existe en nuestra base de datos."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PasswordResetVerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "El código es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscamos una solicitud que coincida con el inicio del token y que no haya expirado
            PasswordReset.objects.get(token__startswith=code.lower(), expires_at__gt=timezone.now())
            # Si la encuentra y no lanza error, el código es válido
            return Response({"detail": "Código válido."}, status=status.HTTP_200_OK)

        except PasswordReset.DoesNotExist:
            return Response(
                {"error": "El código de recuperación es inválido o ha expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Vista para restablecer la contraseña
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Ahora recibimos 'code' en lugar de 'token'
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not all([code, new_password, confirm_password]):
            return Response({"error": "Todos los campos son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Las contraseñas no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscamos la solicitud por la parte inicial del token
            password_reset = PasswordReset.objects.get(token__startswith=code.lower(), expires_at__gt=timezone.now())

            user = password_reset.user
            user.set_password(new_password)
            user.save()
            password_reset.delete()

            return Response(
                {"message": "Tu contraseña ha sido restablecida con éxito."},
                status=status.HTTP_200_OK,
            )

        except PasswordReset.DoesNotExist:
            return Response(
                {"error": "El código de recuperación es inválido o ha expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendVerificationCodeView(APIView):
    """
    Reenvía un nuevo código de activación de forma inteligente.
    - Para Pacientes: Solo requiere el email.
    - Para Profesionales: Requiere email y contraseña para mayor seguridad.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        role = request.data.get("role")
        password = request.data.get("password")  # Puede ser None

        if not email or not role:
            return Response({"error": "El correo y el rol son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        new_code = secrets.token_urlsafe(6).upper()[:6]
        expires_at = timezone.now() + timedelta(minutes=15)

        try:
            if role == "patient":
                target = PreRegistration.objects.get(email=email)

            elif role == "professional":
                if not password:
                    return Response(
                        {"error": "La contraseña es requerida para profesionales."}, status=status.HTTP_400_BAD_REQUEST
                    )

                user = User.objects.get(email=email, role="professional", is_active=False)

                # Verificamos la contraseña como en tu vista original
                if not user.check_password(password):
                    raise exceptions.AuthenticationFailed("Credenciales incorrectas.")

                target = user

            else:
                return Response({"error": "Rol de usuario no válido."}, status=status.HTTP_400_BAD_REQUEST)

            # Actualiza el código y la expiración
            target.verification_code = new_code
            target.verification_code_expires_at = expires_at
            target.save()

            # Envía el nuevo correo
            send_verification_email(target.email, new_code)

            return Response({"message": "Se ha enviado un nuevo código de verificación."}, status=status.HTTP_200_OK)

        except (PreRegistration.DoesNotExist, User.DoesNotExist):
            return Response(
                {"error": "No se encontró una cuenta pendiente de activación para este correo."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except exceptions.AuthenticationFailed as e:
            return Response({"error": str(e.detail)}, status=e.status_code)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        user = self.request.user

        if self.request.method == "PATCH":
            if user.role == "patient":
                return PatientProfileUpdateSerializer
            # Añadir serializer para profesionales si lo necesitas

        if user.role == "professional":
            return ProfessionalProfileSerializer
        elif user.role == "patient":
            return PatientSerializer

        raise exceptions.PermissionDenied("Rol de usuario no soportado.")

    def get_object(self):
        user = self.request.user
        if user.role == "professional":
            return user.professional_profile
        elif user.role == "patient":
            return user.patient_profile
        raise exceptions.NotFound("No se encontró el perfil asociado a este usuario.")

    def update(self, request, *args, **kwargs):
        print("--- DATOS RECIBIDOS EN EL SERVIDOR (PATCH) ---")
        print(f"request.data: {request.data}")
        print(f"request.FILES: {request.FILES}")
        print(f"Content-Type: {request.content_type}")
        print("---------------------------------------------")

        partial = kwargs.pop("partial", True)  # ✅ Siempre usar partial=True para PATCH
        instance = self.get_object()

        # ✅ IMPORTANTE: Pasar el contexto de la request al serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # ✅ Forzar la recarga del objeto para obtener los datos actualizados
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        # Devolver la respuesta con la URL actualizada
        return Response(serializer.data)


class RegenerateLinkCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        professional_profile = user.professional_profile
        today = timezone.now().date()

        # 1. LOGICA DEL LÍMITE DIARIO
        # Si la última actualización NO fue hoy, reinicia el contador.
        if professional_profile.link_code_last_updated != today:
            professional_profile.link_code_changes_today = 0
            professional_profile.link_code_last_updated = today

        # 2. VERIFICACIÓN DEL LÍMITE
        MAX_CHANGES = 3
        if professional_profile.link_code_changes_today >= MAX_CHANGES:
            return Response(
                {"detail": "Límite diario de cambio de código alcanzado."}, status=status.HTTP_403_FORBIDDEN
            )

        # 3. GENERACIÓN Y GUARDADO
        new_link_code = secrets.token_urlsafe(6).upper()[:8]  # Nuevo código
        professional_profile.link_code = new_link_code
        professional_profile.link_code_changes_today += 1  # Incrementa el contador
        professional_profile.save()

        # 4. Devuelve la nueva información
        return Response(
            {
                "message": "Código de enlace actualizado con éxito.",
                "new_link_code": new_link_code,
                "changes_remaining": MAX_CHANGES - professional_profile.link_code_changes_today,
            },
            status=status.HTTP_200_OK,
        )


class ValidateLinkCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        link_code = request.data.get("link_code")

        if not link_code:
            return Response({"error": "El código de enlace es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professional = Professional.objects.get(link_code=link_code)

            # Devuelve el ID del profesional. Usamos el PK del perfil profesional.
            return Response(
                {"professional_id": professional.pk, "message": "Código válido."}, status=status.HTTP_200_OK
            )

        except Professional.DoesNotExist:
            return Response(
                {"error": "Código de enlace inválido. No existe un profesional con ese código."},
                status=status.HTTP_404_NOT_FOUND,
            )


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Reemplaza la vista de login por defecto para usar nuestro serializer personalizado.
    """

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.GenericAPIView):
    """
    Endpoint para que un usuario autenticado cambie su propia contraseña.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Contraseña actualizada con éxito."}, status=status.HTTP_200_OK)


class RequestEmailChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestEmailChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_email = serializer.validated_data["new_email"]

        # Eliminar solicitudes anteriores para este usuario
        EmailChangeRequest.objects.filter(user=user).delete()

        # Crear código y solicitud
        code = secrets.token_hex(3).upper()  # Genera un código de 6 caracteres
        email_request = EmailChangeRequest.objects.create(
            user=user, new_email=new_email, expires_at=timezone.now() + timedelta(minutes=5)
        )
        email_request.set_code(code)
        email_request.save()

        send_verification_change_email(new_email, code)

        return Response(
            {"detail": f"Se ha enviado un código de verificación a {new_email}."}, status=status.HTTP_200_OK
        )


class ConfirmEmailChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmEmailChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_email = serializer.validated_data["new_email"]
        code = serializer.validated_data["verification_code"]

        try:
            # email_request = EmailChangeRequest.objects.get(user=user, new_email__iexact=new_email)
            # Usamos filter().latest() para obtener la solicitud más reciente porque podría haber múltiples entradas
            email_request = EmailChangeRequest.objects.filter(user=user, new_email__iexact=new_email).latest(
                "created_at"
            )
            if email_request.is_expired():
                raise exceptions.ValidationError("El código de verificación ha expirado.")

            if not email_request.check_code(code):
                raise exceptions.ValidationError("El código de verificación es incorrecto.")

            # ¡Éxito! Actualizamos el email del usuario
            user.email = new_email
            user.save()

            # Limpiamos la solicitud
            email_request.delete()

            return Response(
                {"detail": "Tu correo electrónico ha sido actualizado con éxito."}, status=status.HTTP_200_OK
            )

        except EmailChangeRequest.DoesNotExist:
            raise exceptions.ValidationError("No se encontró una solicitud de cambio de correo válida.")


class DeleteAccountView(generics.GenericAPIView):
    """
    Endpoint para que un usuario autenticado elimine su propia cuenta.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Si el serializer es válido, la contraseña es correcta.
        # Procedemos a eliminar el usuario.
        user = request.user
        user.delete()

        return Response({"detail": "Tu cuenta ha sido eliminada permanentemente."}, status=status.HTTP_204_NO_CONTENT)
