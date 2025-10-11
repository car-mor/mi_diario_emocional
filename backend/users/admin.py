from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import EmailChangeRequest, PasswordReset, Patient, Professional, User
from .services import send_approval_email, send_rejection_email


# 1. Definir los modelos de perfil en línea (para verlos en el UserAdmin)
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = "Perfil de Paciente"


class ProfessionalInline(admin.StackedInline):
    model = Professional
    can_delete = False
    verbose_name_plural = "Perfil de Profesional"


# 2. Configurar el Admin del Usuario Base (User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (PatientInline, ProfessionalInline)
    readonly_fields = ("created_at", "verification_code")

    list_display = ("email", "role", "is_active", "is_staff", "created_at")

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
        ("Fechas Importantes", {"fields": ("last_login", "created_at")}),
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
    readonly_fields = ("get_full_name", "get_email", "validate_license_link", "get_registration_date")
    fields = ("get_full_name", "get_email", "validate_license_link", "review_status", "get_registration_date")

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
        return obj.user.created_at

    @admin.display(description="Validar Cédula")
    def validate_license_link(self, obj):
        """Crea un enlace clickeable para validar la cédula en el sitio oficial."""
        if obj.professional_license:
            url = f"https://www.cedulaprofesional.sep.gob.mx/cedula/presidencia/indexA.action?cedula={obj.professional_license}"
            return format_html(
                '<a href="{}" target="_blank">Validar Cédula {} en el portal oficial</a>', url, obj.professional_license
            )
        return "No proporcionada"

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


# 3. Registrar los modelos
admin.site.register(User, CustomUserAdmin)
admin.site.register(PasswordReset)
admin.site.register(EmailChangeRequest)
admin.site.register(Patient)
