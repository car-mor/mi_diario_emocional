from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.html import format_html

from .models import EmailChangeRequest, PasswordReset, Patient, Professional, User
from .services import send_approval_email, send_rejection_email


# 1. Definir los modelos de perfil en línea (para verlos en el UserAdmin)
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = "Perfil de Paciente"

    fields = (
        "professional",
        "alias",
        "gender",
        "description",
        "profile_picture",
        "linked_at",
        "unlinked_at",
        "first_entry_date",
        "current_streak",
        "last_entry_date",
    )
    readonly_fields = ("linked_at", "unlinked_at", "first_entry_date", "last_entry_date", "current_streak")

    raw_id_fields = ("professional",)


class ProfessionalInline(admin.StackedInline):
    model = Professional
    can_delete = False
    verbose_name_plural = "Perfil de Profesional"
    fields = (
        "professional_license",
        "curp",
        "sex",
        "career",
        "institution",
        "review_status",  # Dejamos este editable
        "link_code",
        "link_code_changes_today",
        "link_code_last_updated",
    )

    readonly_fields = (
        "professional_license",
        "curp",
        "sex",
        "career",
        "institution",
        "link_code",
        "link_code_changes_today",
        "link_code_last_updated",
    )


# 2. Configurar el Admin del Usuario Base (User)
class CustomUserAdmin(BaseUserAdmin):
    # inlines = (PatientInline, ProfessionalInline)
    def get_inlines(self, request, obj=None):
        """
        Muestra el inline correcto basado en el rol del usuario.
        """
        if not obj:  # Si es un usuario nuevo
            return []
        if obj.role == "patient":
            return (PatientInline,)
        if obj.role == "professional":
            return (ProfessionalInline,)
        return []  # Los Admins/Superusers no tienen inline

    readonly_fields = ("created_at", "verification_code", "terms_accepted_at")

    list_display = ("email", "role", "is_active", "is_staff", "created_at", "terms_accepted_at")

    list_filter = ("role", "is_active", "is_staff")

    search_fields = ("email", "name", "paternal_last_name")

    # O, si no lo necesitas, simplemente no lo incluyas:
    ordering = ("email",)

    # Define la estructura de campos en el formulario de detalle
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Información Personal",
            {"fields": ("name", "paternal_last_name", "maternal_last_name", "date_of_birth", "role")},
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "verification_code",
                    "verification_code_expires_at",
                )
            },
        ),  # Añadimos campos de verificación
        # CORRECCIÓN AQUÍ: Cambiamos 'date_joined' por 'created_at'
        ("Fechas Importantes", {"fields": ("last_login", "created_at", "terms_accepted_at")}),
    )

    # También debes corregir el método add_fieldsets para la página de creación de usuario admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "password_confirmation",
                    "name",
                    "role",
                ),  # Asegúrate de incluir los REQUIRED_FIELDS
            },
        ),
    )


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("get_full_name", "get_email", "review_status", "get_registration_date")
    list_filter = ("review_status",)
    search_fields = ("user__name", "user__paternal_last_name", "user__email", "professional_license")

    # Define los campos que se mostrarán en la vista de detalle
    readonly_fields = (
        "get_full_name",
        "get_email",
        "get_date_of_birth",
        "sex",
        "curp",
        "validate_license_link",
        "career",
        "institution",
        "get_registration_date",
    )
    fields = (
        "get_full_name",
        "get_email",
        "get_date_of_birth",
        "sex",
        "curp",
        "validate_license_link",
        "career",
        "institution",
        "get_registration_date",
        "review_status",
    )

    # Agrega las acciones personalizadas
    actions = ["approve_applications", "reject_applications"]

    def get_queryset(self, request):
        # Optimiza la consulta para obtener también los datos del usuario relacionado
        return super().get_queryset(request).select_related("user")

    @admin.display(description="Nombre Completo")
    def get_full_name(self, obj):
        return f"{obj.user.name} {obj.user.paternal_last_name}"

    @admin.display(description="Correo Electrónico")
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description="Fecha de Registro")
    def get_registration_date(self, obj):
        if obj.user.created_at:
            return timezone.template_localtime(obj.user.created_at)
        return None

    @admin.display(description="Validar Cédula")
    def validate_license_link(self, obj):
        """Crea un enlace clickeable para validar la cédula en el sitio oficial."""
        if obj.professional_license:
            url = f"https://www.cedulaprofesional.sep.gob.mx/cedula/presidencia/indexA.action?cedula={obj.professional_license}"
            return format_html(
                '<a href="{}" target="_blank">Validar Cédula {} en el portal oficial</a>', url, obj.professional_license
            )
        return "No proporcionada"

    @admin.display(description="Fecha de Nacimiento")
    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth

    @admin.action(description="Aprobar seleccionados y activar cuentas")
    def approve_applications(self, request, queryset):
        for professional in queryset.filter(review_status=Professional.ReviewStatus.PENDING):
            professional.review_status = Professional.ReviewStatus.APPROVED
            professional.user.is_active = True  # <-- ¡ACTIVAMOS LA CUENTA!
            professional.save()
            professional.user.save()
            send_approval_email(professional.user.email)
        self.message_user(request, "Las cuentas seleccionadas han sido aprobadas y activadas.")

    @admin.action(description="Rechazar solicitudes seleccionadas")
    def reject_applications(self, request, queryset):
        for professional in queryset.filter(review_status=Professional.ReviewStatus.PENDING):
            professional.review_status = Professional.ReviewStatus.REJECTED
            professional.save()
            send_rejection_email(professional.user.email)
        self.message_user(request, "Las solicitudes seleccionadas han sido rechazadas.")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Personaliza la vista del modelo Patient en el panel de administración.
    """

    list_display = ("get_full_name", "alias", "get_email", "get_professional_name")
    search_fields = ("alias", "user__name", "user__paternal_last_name", "user__email")
    list_filter = ("gender", "professional__user__name")

    # Optimiza las consultas para cargar los datos relacionados eficientemente
    list_select_related = ("user", "professional__user")

    # Para la vista de detalle, hacemos que los campos importantes sean de solo lectura
    readonly_fields = ("get_full_name", "get_email", "linked_at", "unlinked_at")

    # Define los campos y su orden en la vista de edición/detalle
    fieldsets = (
        ("Información del Usuario", {"fields": ("get_full_name", "get_email")}),
        ("Perfil del Paciente", {"fields": ("professional", "alias", "gender", "description", "profile_picture")}),
        ("Historial de Vinculación", {"fields": ("linked_at", "unlinked_at")}),
    )

    @admin.display(description="Nombre Completo", ordering="user__name")
    def get_full_name(self, obj):
        return obj.user.get_full_name()

    @admin.display(description="Correo Electrónico", ordering="user__email")
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description="Profesional Asignado", ordering="professional__user__name")
    def get_professional_name(self, obj):
        if obj.professional:
            return obj.professional.user.get_full_name()
        return "No asignado"


# 3. Registrar los modelos
admin.site.register(User, CustomUserAdmin)
admin.site.register(PasswordReset)
admin.site.register(EmailChangeRequest)
# admin.site.register(Patient)
