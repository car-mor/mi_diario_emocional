import secrets

from django.conf import settings
from django.core.mail import send_mail


def send_password_reset_email(user_email: str, code: str):
    """Función para enviar el código de recuperación de contraseña."""

    subject = f"{code} es tu código para restablecer la contraseña en EmoDiary"
    message = (
        f"Hola,\n\n"
        f"Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.\n\n"
        f"Usa el siguiente código para completar el proceso:\n\n"
        f"Código de Verificación: {code}\n\n"
        f"Este código expirará en 5 minutos. Si no solicitaste esto, puedes ignorar este correo de forma segura.\n\n"
        f"Atentamente,\n"
        f"El equipo de EmoDiary"
    )
    html_message = (
        f"<h3>Hola,</h3>"
        f"<p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.</p>"
        f"<p>Usa el siguiente código para completar el proceso:</p>"
        f'<p style="font-size: 24px; font-weight: bold; letter-spacing: 2px;">{code}</p>'
        f"<p>Este código expirará en 5 minutos. Si no solicitaste esto, puedes ignorar este correo de forma segura.</p>"
        f"<br>"
        f"<p>Atentamente,<br>El equipo de EmoDiary</p>"
    )

    try:
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False, html_message=html_message
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo de reseteo de contraseña a {user_email}: {e}")
        return False


def send_verification_email(user_email: str, code: str):
    """Función para enviar el código de verificación por correo."""

    subject = "Confirmación de Cuenta EmoDiary - Código de Verificación"
    message = (
        f"Hola,\n\nGracias por registrarte en EmoDiary. "
        f"Tu código de verificación de cuenta es: {code}\n\n"
        f"Por favor, utilízalo en la aplicación para activar tu cuenta."
    )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Remitente
            [user_email],  # Destinatario
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo a {user_email}: {e}")
        return False


def send_verification_change_email(user_email: str, code: str):
    """Función para enviar el código de verificación por correo."""

    subject = f"{code} es tu código de verificación para EmoDiary"
    message = (
        f"Hola,\n\n"
        f"Hemos recibido una solicitud para cambiar el correo electrónico de tu cuenta a esta dirección.\n\n"
        f"Usa el siguiente código para confirmar el cambio:\n\n"
        f"Código de Verificación: {code}\n\n"
        f"Este código expirará en 5 minutos. Si no solicitaste este cambio, puedes ignorar este correo de forma segura.\n\n"
        f"Atentamente,\n"
        f"El equipo de EmoDiary"
    )
    html_message = (
        f"<h3>Hola,</h3>"
        f"<p>Hemos recibido una solicitud para cambiar el correo electrónico de tu cuenta a esta dirección.</p>"
        f"<p>Usa el siguiente código para confirmar el cambio:</p>"
        f'<p style="font-size: 24px; font-weight: bold; letter-spacing: 2px;">{code}</p>'
        f"<p>Este código expirará en 5 minutos. Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>"
        f"<br>"
        f"<p>Atentamente,<br>El equipo de EmoDiary</p>"
    )

    try:
        send_mail(
            subject,
            message,  # Mensaje de texto plano como fallback
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
            html_message=html_message,  # Mensaje en formato HTML
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo a {user_email}: {e}")
        return False


def generate_verification_code(length=6):
    """
    Genera un código de verificación numérico aleatorio.
    """
    return "".join(secrets.token_urlsafe(6).upper()[:length])


def send_approval_email(user_email: str):
    """Envía un correo notificando que la cuenta ha sido aprobada."""
    subject = "¡Tu cuenta en EmoDiary ha sido aprobada!"
    message = (
        "Hola,\n\nNos complace informarte que tu cuenta de profesional ha sido validada y activada. "
        "Ya puedes iniciar sesión en la aplicación y comenzar a usar todas las herramientas.\n\n"
        "¡Bienvenido/a a EmoDiary!"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
        return True
    except Exception as e:
        print(f"Error al enviar correo de aprobación a {user_email}: {e}")
        return False


def send_rejection_email(user_email: str):
    """Envía un correo notificando que la cuenta ha sido rechazada."""
    subject = "Actualización sobre tu registro en EmoDiary"
    message = (
        "Hola,\n\nDespués de revisar tu solicitud de registro como profesional en EmoDiary, "
        "hemos encontrado inconsistencias y, por el momento, no ha sido aprobada.\n\n"
        "Si crees que esto es un error, por favor, ponte en contacto con nuestro equipo de soporte respondiendo a este correo.\n\n"
        "Lamentamos los inconvenientes."
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
        return True
    except Exception as e:
        print(f"Error al enviar correo de rechazo a {user_email}: {e}")
        return False
