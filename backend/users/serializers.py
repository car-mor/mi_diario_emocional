import re
import secrets
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.templatetags.static import static
from django.utils import timezone
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient, PreRegistration, Professional, User
from .services import generate_verification_code


class UserSerializer(serializers.ModelSerializer):
    terms_accepted = serializers.BooleanField(write_only=True)

    email = serializers.EmailField(
        validators=[
            UniqueValidator(  # <-- QUITA 'serializers.' de aquí
                queryset=User.objects.all(), message="Este correo electrónico ya está en uso."
            )
        ]
    )

    class Meta:
        model = User
        # Excluimos la contraseña y el id en la lectura
        fields = [
            "id",
            "email",
            "name",
            "paternal_last_name",
            "maternal_last_name",
            "date_of_birth",
            "role",
            "password",
            "terms_accepted",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "role": {"read_only": True},  # El rol se define al crear el perfil de paciente o profesional
        }

    def validate_name(self, value):
        if not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El nombre debe tener entre 2 y 40 caracteres.")
        return value

    def validate_paternal_last_name(self, value):
        if not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El apellido paterno debe tener entre 2 y 40 caracteres.")
        return value

    def validate_maternal_last_name(self, value):
        # El apellido materno es opcional, así que solo validamos si SÍ se proporcionó.
        if value and not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El apellido materno debe tener entre 2 y 40 caracteres.")
        return value

    def validate_email(self, value):
        """
        Comprueba que el email no esté en uso en la tabla User
        ni en la tabla PreRegistration.
        """
        normalized_email = value.lower()

        # 1. Comprueba contra usuarios ya creados (is_active=True o False)
        #    (El 'unique=True' del modelo ya hace esto, pero ser explícito es bueno)
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")

        # 2. Comprueba contra pacientes pendientes de verificación
        if PreRegistration.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya está en uso por una cuenta pendiente de verificación."
            )

        return value

    def validate_password(self, value):
        errors = []
        if not (8 <= len(value) <= 32):
            errors.append("Debe tener entre 8 y 32 caracteres.")
        if not re.search(r"[A-Z]", value):
            errors.append("Debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            errors.append("Debe contener al menos una letra minúscula.")
        if not re.search(r"\d", value):  # <-- REGLA AÑADIDA
            errors.append("Debe contener al menos un número.")
        if not re.search(r"[@$!%*?&]", value):  # Asegúrate que coincida con tu frontend
            errors.append("Debe contener al menos un carácter especial (@$!%*?&).")

        if errors:
            # Devuelve todos los errores encontrados
            raise serializers.ValidationError(errors)

        return value  # Devuelve la contraseña si es válida

    # Sobreescribimos el método create para hashear la contraseña
    def create(self, validated_data):
        terms = validated_data.pop("terms_accepted", False)
        if not terms:
            raise serializers.ValidationError("Debes aceptar los términos y condiciones para registrarte.")

        password = validated_data.pop("password")

        # Generar un código aleatorio y seguro de 6 caracteres
        new_code = secrets.token_urlsafe(6).upper()[:6]
        expires_at = timezone.now() + timedelta(minutes=15)

        # Crear el objeto User con el código y la expiración
        user = User(**validated_data)
        user.set_password(password)

        user.terms_accepted_at = timezone.now()

        # Asignar el código de verificación y su expiración
        user.verification_code = new_code
        user.verification_code_expires_at = expires_at

        user.save()

        # Llamar inmediatamente al servicio de correo
        from .services import send_verification_email

        send_verification_email(user.email, new_code)

        return user


class ProfessionalSerializer(serializers.ModelSerializer):
    # Anidamos el serializador de User para manejar la creación de ambos modelos
    user = UserSerializer()

    professional_license = serializers.CharField(
        max_length=64,  # Es bueno poner el max_length aquí
        validators=[
            UniqueValidator(queryset=Professional.objects.all(), message="Esta cédula profesional ya está registrada.")
        ],
    )

    curp = serializers.CharField(
        max_length=18,  # Es bueno poner el max_length aquí
        validators=[UniqueValidator(queryset=Professional.objects.all(), message="Este CURP ya está registrado.")],
    )

    class Meta:
        model = Professional
        fields = [
            "user",
            "professional_license",
            "curp",
            "sex",
            "career",
            "institution",
            "link_code",
        ]

        extra_kwargs = {
            "link_code": {"read_only": True},  # El link_code se genera automáticamente
        }

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        # Asignamos el rol 'professional' al usuario
        user_data["role"] = "professional"
        user = UserSerializer().create(validated_data=user_data)
        link_code = secrets.token_urlsafe(6).upper()
        professional = Professional.objects.create(
            user=user,
            link_code=link_code,  # <-- Le pasamos el código generado
            **validated_data,
        )
        return professional


class PatientSerializer(serializers.ModelSerializer):
    # Definimos el campo para que el Serializer sepa manejar el UUID entrante
    professional_id = serializers.UUIDField(write_only=True)

    # Anidamos el serializador de User para manejar la creación de ambos modelos
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = [
            "user",
            "professional",
            "alias",
            "gender",
            "description",
            "profile_picture",
            "linked_at",
            "unlinked_at",
            "professional_id",  # Campo para recibir el ID del profesional
        ]
        extra_kwargs = {
            "description": {"required": False},
            "profile_picture": {"required": False},
            "linked_at": {"read_only": True},
            "unlinked_at": {"read_only": True},
        }

    def create(self, validated_data):
        # 1. Extraer los datos de las relaciones y el anidamiento
        user_data = validated_data.pop("user")
        professional_id = validated_data.pop("professional_id")

        # 2. Convertir UUID en instancia de Modelo Professional
        from .models import Professional

        try:
            professional_instance = Professional.objects.get(user_id=professional_id)
        except Professional.DoesNotExist:
            raise serializers.ValidationError({"professional_id": "El ID del profesional no es válido."})

        # 3. Crear la Instancia de Usuario (Usando el Serializador Anidado)
        user_data["role"] = "patient"
        # Usamos el serializador UserSerializer para crear la instancia de User
        user_instance = UserSerializer().create(validated_data=user_data)

        # 4. Crear el Perfil del Paciente (Patient)
        # Aquí DRF llama a Patient.objects.create(user=user_instance, professional=professional_instance, **validated_data)
        patient = Patient.objects.create(
            user=user_instance,
            professional=professional_instance,
            linked_at=timezone.now(),  # ← AGREGAR ESTA LÍNEA
            **validated_data,
        )

        return patient


class ProfessionalProfileSerializer(serializers.ModelSerializer):
    # Campos del modelo User (usuario base)
    name = serializers.CharField(source="user.name")
    paternal_last_name = serializers.CharField(source="user.paternal_last_name")
    maternal_last_name = serializers.CharField(source="user.maternal_last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Professional
        # Incluimos los campos de User a través del source y los campos de Professional
        fields = ["name", "paternal_last_name", "maternal_last_name", "email", "sex", "link_code"]
        # Los campos que queremos mostrar
        read_only_fields = fields


class PatientProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    paternal_last_name = serializers.CharField(source="user.paternal_last_name")
    maternal_last_name = serializers.CharField(source="user.maternal_last_name")
    email = serializers.EmailField(source="user.email")
    professional_name = serializers.CharField(source="professional.user.name", read_only=True, allow_null=True)

    profile_picture_url = serializers.SerializerMethodField(method_name="get_profile_picture_url")
    is_linked = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "name",
            "paternal_last_name",
            "maternal_last_name",
            "email",
            "alias",
            "gender",
            "professional_name",
            "description",
            "profile_picture_url",
            "is_linked",
            "current_streak",
        ]
        read_only_fields = fields

    # --- CAMBIO 2: Lógica de la URL corregida ---
    def get_profile_picture_url(self, obj):  # o get_avatar_full_url
        # 1. Si SÍ tiene foto, devuelve la URL de DigitalOcean.
        if obj.profile_picture and hasattr(obj.profile_picture, "url"):
            return obj.profile_picture.url

        # 2. Si NO tiene foto, devuelve None.
        # El frontend (Vercel) se encargará de mostrar el /images/avatar-icon.png local.
        return None

    def get_is_linked(self, obj):
        """Devuelve true si el paciente está vinculado a un profesional."""
        return obj.professional is not None


class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = ["alias", "description", "profile_picture", "profile_picture_url"]
        extra_kwargs = {
            "alias": {"required": False},
            "description": {"required": False},
            "profile_picture": {"required": False, "allow_null": True, "write_only": True},
        }

    def validate_alias(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("El alias no puede consistir solo en espacios.")
        if len(value) > 40:
            raise serializers.ValidationError("El alias no puede exceder los 40 caracteres.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("El alias debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=~`/\\[\]]', value):
            raise serializers.ValidationError("El alias debe contener al menos un carácter especial.")

        return value

    def validate_profile_picture(self, value):
        """Validar el tamaño del archivo de imagen"""
        if value:
            # Límite de 50MB
            max_size = 50 * 1024 * 1024  # 50MB en bytes

            if value.size > max_size:
                raise serializers.ValidationError(
                    f"El archivo es demasiado grande. Tamaño máximo: 50MB. "
                    f"Tamaño actual: {value.size / (1024 * 1024):.2f}MB"
                )

            # Validar tipo de archivo
            valid_mime_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
            if value.content_type not in valid_mime_types:
                raise serializers.ValidationError("Formato de imagen no válido. Usa JPG, PNG, GIF o WEBP.")

        return value

    def get_profile_picture_url(self, obj):  # o get_avatar_full_url
        # 1. Si SÍ tiene foto, devuelve la URL de DigitalOcean.
        if obj.profile_picture and hasattr(obj.profile_picture, "url"):
            return obj.profile_picture.url

        # 2. Si NO tiene foto, devuelve None.
        # El frontend (Vercel) se encargará de mostrar el /images/avatar-icon.png local.
        return None

    def update(self, instance, validated_data):
        """Manejar la actualización del perfil"""
        # Actualizar alias
        if "alias" in validated_data:
            instance.alias = validated_data["alias"]

            # Actualizar descripción
        if "description" in validated_data:
            instance.description = validated_data["description"]

        request = self.context.get("request")

        # Verificar si viene el flag de eliminación
        delete_picture = request.data.get("delete_picture") == "true"

        if delete_picture:
            # Eliminar la foto
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
            instance.profile_picture = None
        elif "profile_picture" in validated_data:
            # Subir nueva foto
            new_picture = validated_data.get("profile_picture")
            if new_picture:
                if instance.profile_picture:
                    instance.profile_picture.delete(save=False)
                instance.profile_picture = new_picture

        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado que:
    1. Valida las credenciales manualmente.
    2. Proporciona un error específico si la cuenta no está activa.
    3. Enriquece la respuesta del token con el rol y el estado de revisión.
    """

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # --- Paso 1: Autenticación Manual (Tu lógica original, que es correcta) ---
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Credenciales incorrectas.")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Credenciales incorrectas.")

        # --- Paso 2: Lógica Personalizada de Cuenta Activa (Tu lógica original) ---
        if not user.is_active:
            detail = {
                "code": "account_not_active",
                "detail": "Tu cuenta aún no ha sido activada. Por favor, revisa tu correo para validarla.",
                "role": user.role,  # <-- La pista que necesitamos para el frontend
            }
            raise exceptions.AuthenticationFailed(detail)

        # --- Paso 3: Generar los Tokens y Añadir Datos Extra (La combinación) ---
        self.user = user
        refresh = self.get_token(self.user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # Añadimos el rol del usuario a la respuesta.
        data["role"] = self.user.role

        # Si el usuario es un profesional, añadimos su estado de revisión.
        if self.user.role == "professional":
            try:
                profile = self.user.professional_profile
                data["review_status"] = profile.review_status
            except Professional.DoesNotExist:
                data["review_status"] = None  # O manejar como un error si se prefiere
        # ------------------------------------

        return data


class PreRegistrationSerializer(serializers.ModelSerializer):
    # Campos del modelo User
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    paternal_last_name = serializers.CharField(write_only=True)
    maternal_last_name = serializers.CharField(write_only=True, allow_blank=True)
    date_of_birth = serializers.DateField(write_only=True)
    role = serializers.CharField(write_only=True, initial="patient")
    terms_accepted = serializers.BooleanField(write_only=True)

    # Campos del modelo Patient
    alias = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)
    professional_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = PreRegistration
        # Los `fields` son los campos que se guardarán en el modelo PreRegistration.
        fields = [
            "email",
            "password",
            "name",
            "paternal_last_name",
            "maternal_last_name",
            "date_of_birth",
            "role",
            "alias",
            "gender",
            "hashed_password",
            "user_data",
            "profile_data",
            "verification_code",
            "verification_code_expires_at",
            "professional_id",
            "terms_accepted",
        ]
        # Estos campos son de solo lectura porque los calculamos nosotros.
        read_only_fields = [
            "hashed_password",
            "user_data",
            "profile_data",
            "verification_code",
            "verification_code_expires_at",
        ]

    def validate_alias(self, value):
        """
        Valida el alias:
        - No puede estar vacío o ser solo espacios.
        - Longitud entre 1 y 28 caracteres (Python cuenta bien los emojis).
        """
        if not value.strip():
            raise serializers.ValidationError("El alias es obligatorio y no puede consistir solo en espacios.")

        if not (1 <= len(value) <= 28):
            raise serializers.ValidationError("El alias debe tener entre 1 y 28 caracteres.")

        # Como no hay más reglas, se permiten emojis, números y letras.
        return value

    def validate_name(self, value):
        if not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El nombre debe tener entre 2 y 40 caracteres.")
        return value

    def validate_paternal_last_name(self, value):
        if not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El apellido paterno debe tener entre 2 y 40 caracteres.")
        return value

    def validate_maternal_last_name(self, value):
        # El apellido materno es opcional, así que solo validamos si SÍ se proporcionó.
        if value and not (2 <= len(value) <= 40):
            raise serializers.ValidationError("El apellido materno debe tener entre 2 y 40 caracteres.")
        return value

    def validate_email(self, value):
        """
        Comprueba que el email no esté en uso en la tabla User
        ni en la tabla PreRegistration.
        """
        normalized_email = value.lower()

        # 1. Comprueba contra usuarios ya creados (Terapeutas)
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")

        # 2. Comprueba contra otros pacientes pendientes
        #    (Usamos 'self.instance' para excluir el registro actual si se está actualizando)
        query = PreRegistration.objects.filter(email__iexact=normalized_email)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya está en uso por una cuenta pendiente de verificación."
            )

        return value

    def validate_password(self, value):
        errors = []
        if not (8 <= len(value) <= 32):
            errors.append("Debe tener entre 8 y 32 caracteres.")
        if not re.search(r"[A-Z]", value):
            errors.append("Debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            errors.append("Debe contener al menos una letra minúscula.")
        if not re.search(r"\d", value):  # <-- REGLA AÑADIDA
            errors.append("Debe contener al menos un número.")
        if not re.search(r"[@$!%*?&]", value):  # Asegúrate que coincida con tu frontend
            errors.append("Debe contener al menos un carácter especial (@$!%*?&).")

        if errors:
            # Devuelve todos los errores encontrados
            raise serializers.ValidationError(errors)

        return value  # Devuelve la contraseña si es válida

    def validate_date_of_birth(self, value):
        """
        Valida la fecha de nacimiento.
        - No puede ser en el futuro.
        - Debe ser mayor de 18 años.
        - No puede ser mayor de 120 años.
        """
        today = date.today()
        if value > today:
            raise serializers.ValidationError("La fecha de nacimiento no puede ser en el futuro.")

        # Calcular edad
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        # 1. Límite de 120 años (NUEVA VALIDACIÓN)
        if age > 120:
            raise serializers.ValidationError("La fecha de nacimiento no es válida (supera los 120 años).")

        # 2. Mínimo 18 años
        if age < 18:
            raise serializers.ValidationError("Debes ser mayor de 18 años para registrarte.")

        return value

    def create(self, validated_data):
        """
        Sobrescribimos el método `create` para que actualice un pre-registro
        existente o cree uno nuevo si no existe.
        """

        terms = validated_data.pop("terms_accepted", False)
        if not terms:
            # Esta validación se activa si el frontend no envía 'terms_accepted: true'
            raise serializers.ValidationError("Debes aceptar los términos y condiciones para registrarte.")

        email = validated_data.get("email")

        # Datos que se usarán para crear o actualizar el registro
        defaults = {
            "hashed_password": make_password(validated_data.get("password")),
            "user_data": {
                "name": validated_data.get("name"),
                "paternal_last_name": validated_data.get("paternal_last_name"),
                "maternal_last_name": validated_data.get("maternal_last_name") or None,
                "date_of_birth": str(validated_data.get("date_of_birth")),
            },
            "profile_data": {
                "alias": validated_data.get("alias"),
                "gender": validated_data.get("gender"),
                "professional_id": str(validated_data.get("professional_id")),
            },
            "terms_accepted": True,
            "role": "patient",
            "verification_code": generate_verification_code(),  # Genera un nuevo código siempre
            "verification_code_expires_at": timezone.now() + timedelta(minutes=15),
        }

        # Usamos update_or_create para manejar el caso de duplicados
        # Busca por 'email' y si lo encuentra, lo actualiza con 'defaults'.
        # Si no lo encuentra, crea uno nuevo con todos los datos.
        pre_registration, created = PreRegistration.objects.update_or_create(email=email, defaults=defaults)

        return pre_registration


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para el cambio de contraseña de un usuario autenticado.
    """

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        # 1. Comprobar que la nueva contraseña y su confirmación coincidan
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Las nuevas contraseñas no coinciden."})

        # 2. Comprobar que la contraseña actual sea correcta
        user = self.context["request"].user
        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError({"current_password": "La contraseña actual es incorrecta."})

        # 2. Validar que la vieja contraseña no sea igual a la nueva
        if data["current_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "La nueva contraseña no puede ser igual a la actual."})

        # 3. Validar la nueva contraseña con las reglas de Django
        try:
            validate_password(data["new_password"], user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data

    def save(self, **kwargs):
        # El método save se llamará solo si la validación es exitosa
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class RequestEmailChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_email = serializers.EmailField(required=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def validate_new_email(self, value):
        # Normalizar y comprobar que no esté ya en uso
        normalized_email = value.lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("Esta dirección de correo electrónico ya está en uso.")
        return normalized_email


class ConfirmEmailChangeSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True, max_length=6)


class DeleteAccountSerializer(serializers.Serializer):
    """
    Serializer para validar la contraseña al eliminar la cuenta.
    """

    password = serializers.CharField(required=True)

    def validate_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña es incorrecta.")
        return value


class PatientListSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar una lista de pacientes a un profesional.
    """

    # Obtenemos campos del modelo User relacionado
    name = serializers.CharField(source="user.get_full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    # Calculamos la edad dinámicamente
    age = serializers.SerializerMethodField()

    # Construimos la URL completa del avatar
    avatar_url = serializers.SerializerMethodField(method_name="get_avatar_full_url")
    id = serializers.UUIDField(source="user.id", read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "name", "age", "gender", "email", "alias", "avatar_url"]

    def get_age(self, obj):
        today = date.today()
        born = obj.user.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# --- CAMBIO 6: Lógica de URL corregida ---
def get_avatar_full_url(self, obj):
    # 1. Si SÍ tiene foto, devuelve la URL de DigitalOcean.
    if obj.profile_picture and hasattr(obj.profile_picture, "url"):
        return obj.profile_picture.url

    # 2. Si NO tiene foto, devuelve None.
    # El frontend (Vercel) se encargará de mostrar el /images/avatar-icon.png local.
    return None
