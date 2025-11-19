# Create your models here.
import logging
import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


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
        """Actualiza la racha basándose en TODAS las entradas históricas - VERSIÓN CORREGIDA"""
        import logging

        from django.utils import timezone

        logger = logging.getLogger(__name__)

        today = timezone.now().date()
        logger.debug(f"🚀 CALCULANDO RACHA COMPLETA para {self.alias} - Hoy: {today}")

        # Obtener TODAS las entradas usando el related_name
        entries = self.diary_entries.all().order_by("entry_date")

        # DEBUG: Mostrar todas las entradas con comparación de fechas
        logger.debug(f"🔍 DIAGNÓSTICO COMPLETO para {self.alias}:")
        for entry in entries:
            utc_time = entry.entry_date
            local_time = timezone.localtime(utc_time)
            naive_date = utc_time.date()  # ¡INCORRECTO!
            local_date = local_time.date()  # ✅ CORRECTO

            logger.debug(f"   - UTC: {utc_time}")
            logger.debug(f"     Local: {local_time} -> Fecha: {local_date}")
            logger.debug(f"     Naive: {naive_date} -> {'❌ PROBLEMA' if naive_date != local_date else '✅ OK'}")
            logger.debug(f"     Título: {entry.title}")

        if not entries:
            # Primera entrada del usuario
            self.current_streak = 1
            self.first_entry_date = today
            self.last_entry_date = today
            self.save()
            logger.info(f"✅ PRIMERA ENTRADA - {self.alias}: Streak = 1")
            return

        # ✅ CORREGIDO: Usar timezone.localtime() para obtener la fecha correcta
        entry_dates = set()
        for entry in entries:
            # ¡ESTA ES LA LÍNEA CLAVE CORREGIDA!
            local_datetime = timezone.localtime(entry.entry_date)
            local_date = local_datetime.date()
            entry_dates.add(local_date)

        # Convertir a lista ordenada
        unique_dates = sorted(list(entry_dates))
        logger.debug(f"📅 Fechas de entradas únicas (CORREGIDAS): {unique_dates}")

        # Calcular la secuencia consecutiva MÁS LARGA
        longest_streak = 1
        current_streak = 1

        for i in range(1, len(unique_dates)):
            days_diff = (unique_dates[i] - unique_dates[i - 1]).days

            if days_diff == 1:
                # Día consecutivo - incrementar racha actual
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                # Break en la secuencia - reiniciar racha actual
                current_streak = 1

        logger.debug(f"📊 Cálculo completo - Racha más larga: {longest_streak}")

        # Verificar si la entrada de hoy extiende la racha
        latest_entry_date = unique_dates[-1] if unique_dates else None
        has_entry_today = today in unique_dates

        if has_entry_today:
            # Si ya hay entrada hoy, usar la racha calculada
            new_streak = longest_streak
            logger.debug(f"🔄 Entrada hoy ya existe - Usar racha calculada: {new_streak}")
        else:
            # Si es nueva entrada hoy, verificar si extiende la racha
            if latest_entry_date and (today - latest_entry_date).days == 1:
                new_streak = longest_streak + 1
                logger.debug(f"📈 Día consecutivo - Nueva racha: {new_streak}")
            else:
                new_streak = 1
                logger.debug(f"🆕 Nueva racha o break - Racha: {new_streak}")

        # Actualizar todos los campos
        old_streak = self.current_streak
        self.current_streak = new_streak
        self.last_entry_date = today

        # Actualizar first_entry_date si es necesario
        if not self.first_entry_date and unique_dates:
            self.first_entry_date = unique_dates[0]

        self.save()

        if old_streak != new_streak:
            logger.info(f"🎯 RACHA ACTUALIZADA: {self.alias} - {old_streak} → {new_streak}")
        else:
            logger.info(f"ℹ️  RACHA MANTENIDA: {self.alias} - {new_streak}")

    def verify_streak_consistency(self):
        """Verificación rápida - ahora update_streak_on_new_entry ya hace el cálculo completo"""

        logger = logging.getLogger(__name__)

        # Simplemente registrar el estado actual
        logger.debug(f"🔍 VERIFICACIÓN: {self.alias} - Streak: {self.current_streak}, Última: {self.last_entry_date}")

        # Podemos llamar a update_streak_on_new_entry para forzar recálculo si queremos
        # self.update_streak_on_new_entry()

        return self.current_streak

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
