# importacion de secrets
import base64
import os
import secrets
import uuid
from collections import Counter
from datetime import date, timedelta

from django.conf import settings  # Para acceder a variables de configuración
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import exceptions, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

# Importa los permisos (esto es clave para proteger tus vistas)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from weasyprint import HTML

from diary.ml_service import NLP, lematizar_texto_para_lista, preprocesar_texto
from diary.models import DiaryEntry
from diary.serializers import DiaryEntrySerializer

from .models import EmailChangeRequest, PasswordReset, Patient, PreRegistration, Professional, User
from .permissions import IsPatient, IsProfessional

STOP_WORDS = NLP.Defaults.stop_words if NLP else set()
# Importa los serializadores y modelos
from .serializers import (
    ChangePasswordSerializer,
    ConfirmEmailChangeSerializer,
    CustomTokenObtainPairSerializer,
    DeleteAccountSerializer,
    PatientListSerializer,
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
                        professional=professional_instance,
                        linked_at=timezone.localtime(),      
                        **profile_data,
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

            # if (
            #     not user.check_password(password)
            #     or user.verification_code != verification_code
            #     or user.verification_code_expires_at < timezone.now()
            # ):
            #     raise User.DoesNotExist
            
            # 1. Comprobar la expiración PRIMERO
            if user.verification_code_expires_at < timezone.now():
                return Response(
                    {"error": "El código de verificación ha expirado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 2. Comprobar credenciales y código
            if (
                not user.check_password(password)
                or user.verification_code != verification_code
            ):
                return Response(
                    {"error": "Credenciales o código de verificación incorrectos."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = True
            user.verification_code = None
            user.verification_code_expires_at = None
            user.save()

            return Response(
                {"message": "Correo de profesional verificado con éxito. Ya puedes iniciar sesión."},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
        # Esta excepción ahora solo se activa si el email NO existe
            return Response(
                {"error": "No se encontró una cuenta profesional pendiente para este correo."},
                status=status.HTTP_404_NOT_FOUND,
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
            return PatientProfileSerializer

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


class ProfessionalActionsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsProfessional]
    serializer_class = PatientListSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "professional_profile"):
            return user.professional_profile.patients.all().select_related("user")
        return Patient.objects.none()

    def retrieve(self, request, *args, **kwargs):
        patient = self.get_object()
        start_date_param = request.query_params.get("start_date")
        end_date_param = request.query_params.get("end_date")

        if start_date_param and end_date_param:
            # MODO PERSONALIZADO: Si se provee un rango, lo usamos.
            start_date = date.fromisoformat(start_date_param)
            end_date = date.fromisoformat(end_date_param)
            # Para el reporte, asumimos que un rango personalizado siempre está "disponible"
            is_report_available = True
            next_report_date = end_date
        else:
            # MODO SEMANAL (por defecto): Usamos la lógica de la semana más reciente.
            start_date, end_date, is_report_available, next_report_date = self._get_most_recent_week_info(patient)
        # ------------------------------------

        diary_entries = DiaryEntry.objects.filter(patient=patient, entry_date__date__range=[start_date, end_date])
        # --- Lógica para la Gráfica de Emociones Combinadas ---
        combination_counts = Counter()
        for entry in diary_entries:
            emotions = entry.analyzed_emotions
            # Solo cuenta si la lista no está vacía Y no es ['neutro']
            if emotions and emotions != ["neutro"]:
                combination = tuple(sorted(emotions))
                combination_counts[combination] += 1
        most_common_combinations = [[" - ".join(comb), count] for comb, count in combination_counts.most_common(5)]
        # --- Lógica para la Nube de Palabras ---
        full_text = " ".join([entry.content for entry in diary_entries])
        if full_text.strip():
            lemmas = lematizar_texto_para_lista(preprocesar_texto(full_text))
            important_words = [
                lemma for lemma in lemmas if lemma not in STOP_WORDS and lemma.isalpha() and len(lemma) > 2
            ]
            word_counts = Counter(important_words)
            most_common_words_raw = word_counts.most_common(50)
        else:
            most_common_words_raw = []

        max_count = most_common_words_raw[0][1] if most_common_words_raw else 0
        min_count = most_common_words_raw[-1][1] if most_common_words_raw else 0
        count_range = float(max_count - min_count)

        most_common_words_with_size = []
        for word, count in most_common_words_raw:
            size_class = "size-1"  # default
            if count_range > 0:
                size_percent = ((count - min_count) / count_range) * 100
                if size_percent > 80:
                    size_class = "size-5"
                elif size_percent > 60:
                    size_class = "size-4"
                elif size_percent > 40:
                    size_class = "size-3"
                elif size_percent > 20:
                    size_class = "size-2"
            elif max_count > 0:  # Solo hay una palabra
                size_class = "size-3"

            most_common_words_with_size.append((word, count, size_class))

        # --- Construye la respuesta JSON final (CORREGIDO) ---
        data = {
            "patient_details": self.get_serializer(patient).data,
            "diary_history": DiaryEntrySerializer(diary_entries, many=True).data,
            "emotion_combinations": most_common_combinations,
            "word_frequency": most_common_words_with_size,
            "report_info": {
                "is_available": is_report_available,
                "next_report_date": next_report_date.strftime("%d de %B de %Y"),
                "is_custom_range": bool(start_date_param),  # Un flag para el frontend
            },
        }
        return Response(data)

    @action(detail=True, methods=["get"], url_path="download-report")
    def download_report(self, request, pk=None):
        patient = self.get_object()
        start_date_param = request.query_params.get("start_date")
        end_date_param = request.query_params.get("end_date")

        if start_date_param and end_date_param:
            start_date = date.fromisoformat(start_date_param)
            end_date = date.fromisoformat(end_date_param)
            if start_date == end_date:
                report_title = f"Resumen del Día ({start_date.strftime('%d %b, %Y')})"
            else:
                report_title = "Resumen de Periodo Personalizado"
        else:
            start_date, end_date, is_available, _ = self._get_most_recent_week_info(patient)
            if not is_available:
                return Response(
                    {"detail": "El reporte semanal aún no está disponible."}, status=status.HTTP_403_FORBIDDEN
                )
            report_title = "Resumen Semanal"

        diary_entries = DiaryEntry.objects.filter(patient=patient, entry_date__date__range=[start_date, end_date])

        # --- AÑADIMOS LA LÓGICA DE CÁLCULO QUE FALTABA ---
        # Lógica para Emociones Combinadas
        combination_counts = Counter()
        for entry in diary_entries:
            emotions = entry.analyzed_emotions
            if emotions and emotions != ["neutro"]:
                combination = tuple(sorted(emotions))
                combination_counts[combination] += 1
        most_common_combinations = [[" - ".join(comb), count] for comb, count in combination_counts.most_common(5)]
        # Lógica para Nube de Palabras
        full_text = " ".join([entry.content for entry in diary_entries])
        if full_text.strip():
            lemmas = lematizar_texto_para_lista(preprocesar_texto(full_text))
            important_words = [
                lemma for lemma in lemmas if lemma not in STOP_WORDS and lemma.isalpha() and len(lemma) > 2
            ]
            word_counts = Counter(important_words)
            most_common_words_raw = word_counts.most_common(50)
        else:
            most_common_words_raw = []

        max_count = most_common_words_raw[0][1] if most_common_words_raw else 0
        min_count = most_common_words_raw[-1][1] if most_common_words_raw else 0
        count_range = float(max_count - min_count)

        most_common_words_with_size = []
        for word, count in most_common_words_raw:
            size_class = "size-1"  # default
            if count_range > 0:
                size_percent = ((count - min_count) / count_range) * 100
                if size_percent > 80:
                    size_class = "size-5"
                elif size_percent > 60:
                    size_class = "size-4"
                elif size_percent > 40:
                    size_class = "size-3"
                elif size_percent > 20:
                    size_class = "size-2"
            elif max_count > 0:  # Solo hay una palabra
                size_class = "size-3"

            most_common_words_with_size.append((word, count, size_class))

        avatar_data_uri = None
        if patient.profile_picture:
            try:
                # 1. Abrir el archivo de la imagen en modo binario
                with open(patient.profile_picture.path, "rb") as image_file:
                    # 2. Leer los bytes y codificarlos a Base64
                    image_bytes = image_file.read()
                    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

                    # 3. Crear el Data URI completo para el HTML
                    # (Tenemos que adivinar el tipo de imagen, usualmente jpeg o png)
                    content_type = (
                        "image/png" if patient.profile_picture.name.lower().endswith(".png") else "image/jpeg"
                    )
                    avatar_data_uri = f"data:{content_type};base64,{image_b64}"

            except (FileNotFoundError, IOError):
                # Si el archivo está roto o no se encuentra, simplemente no se mostrará
                avatar_data_uri = None

        logo_data_uri = None
        try:
            # settings.BASE_DIR apunta a la carpeta 'backend'
            logo_path = os.path.join(settings.BASE_DIR, "media_root", "logo.png")
            with open(logo_path, "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode("utf-8")
                logo_data_uri = f"data:image/png;base64,{image_b64}"
        except (FileNotFoundError, IOError):
            logo_data_uri = None  # El logo es opcional
            
        therapist_name = "No Asignado"
        if patient.professional:
            therapist_name = patient.professional.user.get_full_name()

        context = {
            "patient": patient,
            "therapist_name": therapist_name,
            "diary_entries": diary_entries,
            "avatar_data_uri": avatar_data_uri,
            "logo_data_uri": logo_data_uri,
            "emotion_combinations": most_common_combinations,
            "word_frequency": most_common_words_with_size,
            "week_start": start_date,
            "week_end": end_date,
            "report_title": report_title,
        }

        html_string = render_to_string("reports/weekly_report.html", context)
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_{patient.alias}_{start_date}.pdf"'
        return response

    @action(detail=True, methods=["get"], url_path="report-weeks")
    def report_weeks(self, request, pk=None):
        """
        Devuelve una lista de las semanas de reporte disponibles para un paciente.
        """
        patient = self.get_object()
        
        if not patient.first_entry_date:
            self._get_most_recent_week_info(patient)
            patient.refresh_from_db()
        
        if not patient.first_entry_date:
            return Response([])

        first_date = patient.first_entry_date
        today = timezone.localdate()

        total_days = (today - first_date).days
        if total_days < 0:
            return Response([])

        total_weeks = (total_days // 7) + 1

        weeks_data = []
        for week_num in range(total_weeks):
            start_date = first_date + timedelta(days=week_num * 7)
            end_date = start_date + timedelta(days=6)
            weeks_data.append(
                {
                    "week_number": week_num + 1,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "display_text": f"Semana {week_num + 1} ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')})",
                }
            )

        # Devolvemos las semanas en orden descendente (la más reciente primero)
        return Response(sorted(weeks_data, key=lambda w: w["week_number"], reverse=True))

    def _get_most_recent_week_info(self, patient):
        """Calcula la información de la semana de reporte más reciente."""

        first_date = patient.first_entry_date

        today = timezone.localdate()
        # Lógica mejorada: si la fecha no está establecida, la buscamos.
        if not first_date:
            first_entry = patient.diary_entries.order_by("entry_date").first()
            if first_entry:
                first_date = timezone.localtime(first_entry.entry_date).date()
                # Guardamos la fecha para que la próxima vez sea más rápido
                patient.first_entry_date = first_date
                patient.save()
            else:
                # Si realmente no hay entradas, devolvemos el estado "sin datos".
                return today, today, False, today + timedelta(days=7)

        days_since_first = (today - first_date).days
        
        if days_since_first < 0:
            return today, today, False, first_date + timedelta(days=7)

        current_week_number = days_since_first // 7
        start_date = first_date + timedelta(days=current_week_number * 7)
        end_date = start_date + timedelta(days=6)

        is_report_available = (today >= start_date + timedelta(days=7))
        # O si hoy es el último día de la semana
        if today == end_date:
             is_report_available = True
             
        if current_week_number == 0 and days_since_first >= 7:
            is_report_available = True
            
        is_report_available = (today - start_date).days >= 7
        next_report_date = start_date + timedelta(days=7)

        return start_date, end_date, is_report_available, next_report_date

    @action(detail=True, methods=["post"], url_path="disconnect")
    def disconnect(self, request, pk=None):
        """
        Desvincula un paciente del profesional.
        URL: POST /api/professional/patients/{patient_id}/disconnect/
        """
        # get_object() usa el queryset para asegurar que el profesional
        # solo puede desvincular a un paciente que le pertenece.
        patient_to_disconnect = self.get_object()

        # "Desvincular" en tu modelo significa poner el campo 'professional' a None.
        patient_to_disconnect.professional = None
        patient_to_disconnect.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkToProfessionalView(APIView):
    """
    Permite a un paciente autenticado y no vinculado
    enviar un código para vincularse a un profesional.
    """

    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request, *args, **kwargs):
        link_code = request.data.get("link_code")
        if not link_code:
            return Response({"error": "El código de enlace es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professional_to_link = Professional.objects.get(link_code=link_code)
        except Professional.DoesNotExist:
            return Response({"error": "El código de enlace es inválido."}, status=status.HTTP_404_NOT_FOUND)

        patient_profile = request.user.patient_profile

        # Verificamos si ya está vinculado para evitar re-vinculaciones innecesarias
        if patient_profile.professional:
            return Response({"error": "Ya estás vinculado a un profesional."}, status=status.HTTP_400_BAD_REQUEST)

        # ¡Éxito! Hacemos la vinculación
        patient_profile.professional = professional_to_link
        patient_profile.linked_at = timezone.now()
        patient_profile.save()

        return Response({"message": "Vinculación exitosa."}, status=status.HTTP_200_OK)
