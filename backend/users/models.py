# Create your models here.
import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# Manager para el modelo de usuario personalizado
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Modelo de usuario base
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("patient", "Patient"),
        ("professional", "Professional"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)
    date_of_birth = models.DateField(null=False)
    name = models.CharField(max_length=255, null=False)
    paternal_last_name = models.CharField(max_length=255, null=False)
    maternal_last_name = models.CharField(max_length=255, null=True, blank=True)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

    # Campos para la verificación de cuenta
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expires_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role", "date_of_birth", "name", "paternal_last_name"]

    def get_full_name(self):
        """
        Devuelve el nombre completo del usuario.
        """
        return f"{self.name} {self.paternal_last_name} {self.maternal_last_name}".strip()

    def __str__(self):
        return self.email


class Patient(models.Model):
    GENDER_CHOICES = (
        ("male", "Masculino"),
        ("female", "Femenino"),
        ("non_binary", "No binario"),
        ("other", "Otro"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="patient_profile")
    professional = models.ForeignKey(
        "Professional", on_delete=models.SET_NULL, null=True, blank=True, related_name="patients"
    )
    alias = models.CharField(max_length=32, null=False)
    gender = models.CharField(max_length=16, null=False, choices=GENDER_CHOICES)
    description = models.TextField(default="Ingresa tu descripción aquí", blank=True)
    profile_picture = models.ImageField(upload_to="avatars/", null=True, blank=True)
    linked_at = models.DateTimeField(null=True, blank=True)
    unlinked_at = models.DateTimeField(null=True, blank=True)
    first_entry_date = models.DateField(null=True, blank=True)
    current_streak = models.IntegerField(default=0)
    last_entry_date = models.DateField(null=True, blank=True)

    def update_streak_on_new_entry(self):
        """Actualiza la racha cuando se crea una nueva entrada - Lógica unificada"""
        today = timezone.now().date()

        print(f"DEBUG STREAK: Actualizando racha - Última entrada: {self.last_entry_date}, Hoy: {today}")

        # Si es la primera entrada o no hay última entrada
        if not self.last_entry_date:
            self.current_streak = 1
            self.first_entry_date = today
            print(f"DEBUG STREAK: Primera entrada - Streak: 1")

        else:
            days_diff = (today - self.last_entry_date).days
            print(f"DEBUG STREAK: Diferencia de días: {days_diff}")

            if days_diff == 1:
                # Día consecutivo - incrementar
                self.current_streak += 1
                print(f"DEBUG STREAK: Día consecutivo - Nuevo streak: {self.current_streak}")
            elif days_diff == 0:
                # Mismo día - mantener streak actual
                print(f"DEBUG STREAK: Mismo día - Mantener streak: {self.current_streak}")
            else:
                # Más de 1 día de diferencia - reiniciar
                self.current_streak = 1
                print(f"DEBUG STREAK: Break en la racha - Nuevo streak: 1")

        # Siempre actualizar la última fecha de entrada
        self.last_entry_date = today
        self.save()

        print(f"DEBUG STREAK: Resultado final - Streak: {self.current_streak}, Última entrada: {self.last_entry_date}")

    def verify_streak_consistency(self):
        """Verifica la consistencia de la racha basándose en las entradas reales"""
        from datetime import timedelta

        from django.utils import timezone

        from diary.models import DiaryEntry

        # Obtener todas las entradas ordenadas por fecha
        entries = DiaryEntry.objects.filter(patient=self).order_by("entry_date")

        if not entries:
            return 0

        current_streak = 1
        current_date = timezone.now().date()

        # Empezar desde la entrada más reciente y verificar consecutividad
        for i in range(len(entries) - 1, 0, -1):
            current_entry_date = entries[i].entry_date.date()
            previous_entry_date = entries[i - 1].entry_date.date()

            days_diff = (current_entry_date - previous_entry_date).days

            if days_diff == 1:
                current_streak += 1
            else:
                break

        print(f"DEBUG VERIFICACIÓN: Streak calculado: {current_streak}, Streak en BD: {self.current_streak}")

        return current_streak

    def __str__(self):
        return self.alias


class Professional(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobado"
        REJECTED = "REJECTED", "Rechazado"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="professional_profile")
    professional_license = models.CharField(max_length=64, null=False, unique=True)
    curp = models.CharField(max_length=18, null=False, unique=True)
    sex = models.CharField(max_length=16, null=False)
    career = models.CharField(max_length=255, null=False)
    institution = models.CharField(max_length=255, null=False)
    link_code = models.CharField(max_length=16, null=False, unique=True)
    link_code_changes_today = models.PositiveSmallIntegerField(default=0)
    link_code_last_updated = models.DateField(default=timezone.now)
    review_status = models.CharField(
        max_length=10, choices=ReviewStatus.choices, default=ReviewStatus.PENDING, verbose_name="Estado de Revisión"
    )

    def __str__(self):
        return f"{self.user.name} {self.user.paternal_last_name}"


class PasswordReset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Password reset token for {self.user.email}"


class EmailChangeRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.EmailField()
    # Guardamos el hash del código, no el código en texto plano
    hashed_verification_code = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def set_code(self, raw_code):
        self.hashed_verification_code = make_password(raw_code)

    def check_code(self, raw_code):
        return check_password(raw_code, self.hashed_verification_code)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Solicitud de cambio de email para {self.user.email}"


class PreRegistration(models.Model):
    """
    Modelo para almacenar temporalmente los datos de registro
    hasta que el usuario verifique su email.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=10)
    verification_code_expires_at = models.DateTimeField()
    terms_accepted = models.BooleanField(default=False)

    # Guardamos el resto de los datos como JSON
    user_data = models.JSONField()  # Datos del usuario (name, apellidos, etc.)
    profile_data = models.JSONField()  # Datos del perfil (patient o professional)
    role = models.CharField(max_length=20)  # 'patient' o 'professional'

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_preregistration"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["verification_code"]),
        ]

    def is_code_expired(self):
        """Verifica si el código de verificación ha expirado"""
        return timezone.now() > self.verification_code_expires_at

    def __str__(self):
        return f"PreRegistration: {self.email} ({self.role})"
