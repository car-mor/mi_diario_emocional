import secrets
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.templatetags.static import static
from django.utils import timezone
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient, PreRegistration, Professional, User
from .services import generate_verification_code


class UserSerializer(serializers.ModelSerializer):
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
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "role": {"read_only": True},  # El rol se define al crear el perfil de paciente o profesional
        }

    # Sobreescribimos el método create para hashear la contraseña
    def create(self, validated_data):
        password = validated_data.pop("password")

        # Generar un código aleatorio y seguro de 6 caracteres
        new_code = secrets.token_urlsafe(6).upper()[:6]
        expires_at = timezone.now() + timedelta(minutes=5)

        # Crear el objeto User con el código y la expiración
        user = User(**validated_data)
        user.set_password(password)

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
            user=user_instance,  # Le pasamos la INSTANCIA de User (corregido)
            professional=professional_instance,  # Le pasamos la INSTANCIA de Professional (corregido)
            **validated_data,  # El resto de campos (alias, gender, description, etc.)
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

    profile_picture = serializers.SerializerMethodField()

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
            "profile_picture",
        ]
        read_only_fields = fields

    def get_profile_picture(self, obj):
        request = self.context.get("request")
        if obj.profile_picture and hasattr(obj.profile_picture, "url"):
            return request.build_absolute_uri(obj.profile_picture.url)
        return request.build_absolute_uri(static("images/avatar-icon.png"))


class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = ["description", "profile_picture", "profile_picture_url"]
        extra_kwargs = {
            "description": {"required": False},
            "profile_picture": {"required": False, "allow_null": True},
        }

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

    def get_profile_picture_url(self, obj):
        """Devuelve la URL completa de la foto después de actualizar"""
        request = self.context.get("request")
        if obj.profile_picture and hasattr(obj.profile_picture, "url"):
            return request.build_absolute_uri(obj.profile_picture.url)
        return request.build_absolute_uri(static("images/avatar-icon.png"))

    def update(self, instance, validated_data):
        """Manejar la actualización del perfil"""
        request = self.context.get("request")

        # Verificar si viene el flag de eliminación
        delete_picture = request.data.get("delete_picture") == "true"

        if delete_picture:
            # Eliminar la foto
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
            instance.profile_picture = None
            print("🗑️ Foto eliminada")
        elif "profile_picture" in validated_data:
            # Subir nueva foto
            new_picture = validated_data.get("profile_picture")
            if new_picture:
                if instance.profile_picture:
                    instance.profile_picture.delete(save=False)
                instance.profile_picture = new_picture
                print(f"📸 Nueva foto guardada")

        # Actualizar descripción
        if "description" in validated_data:
            instance.description = validated_data["description"]

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
    # Definimos explícitamente los campos que esperamos del frontend
    # para que el serializador pueda validarlos.
    # Estos campos no existen directamente en el modelo PreRegistration,
    # así que los marcamos como write_only=True.

    # Campos del modelo User
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    paternal_last_name = serializers.CharField(write_only=True)
    maternal_last_name = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    role = serializers.CharField(write_only=True, initial="patient")

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
        ]
        # Estos campos son de solo lectura porque los calculamos nosotros.
        read_only_fields = [
            "hashed_password",
            "user_data",
            "profile_data",
            "verification_code",
            "verification_code_expires_at",
        ]

    def create(self, validated_data):
        """
        Sobrescribimos el método `create` para que actualice un pre-registro
        existente o cree uno nuevo si no existe.
        """
        email = validated_data.get("email")

        # Datos que se usarán para crear o actualizar el registro
        defaults = {
            "hashed_password": make_password(validated_data.get("password")),
            "user_data": {
                "name": validated_data.get("name"),
                "paternal_last_name": validated_data.get("paternal_last_name"),
                "maternal_last_name": validated_data.get("maternal_last_name"),
                "date_of_birth": str(validated_data.get("date_of_birth")),
            },
            "profile_data": {
                "alias": validated_data.get("alias"),
                "gender": validated_data.get("gender"),
                "professional_id": str(validated_data.get("professional_id")),
            },
            "role": "patient",
            "verification_code": generate_verification_code(),  # Genera un nuevo código siempre
            "verification_code_expires_at": timezone.now() + timedelta(minutes=15),
        }

        # Usamos update_or_create para manejar el caso de duplicados
        # Busca por 'email' y si lo encuentra, lo actualiza con 'defaults'.
        # Si no lo encuentra, crea uno nuevo con todos los datos.
        pre_registration, created = PreRegistration.objects.update_or_create(email=email, defaults=defaults)

        return pre_registration
