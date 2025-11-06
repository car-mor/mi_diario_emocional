import secrets

from django.conf import settings
from django.core.mail import send_mail

# --- 1. Plantilla Base de Correo HTML ---
# Usamos CSS "en línea" (style="...") porque Gmail y Outlook
# eliminan las etiquetas <style> por seguridad.

EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    
                    <tr>
                        <td style="padding: 20px; text-align: center; background-color: #f9f9f9; border-bottom: 1px solid #eee;">
                            <h1 style="margin: 0; font-size: 24px; color: #333;">
                                <strong>Mi diario emocional</strong>
                            </h1>
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding: 30px 40px; color: #333; line-height: 1.6;">
                            {content}
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding: 20px 40px; text-align: center; background-color: #f9f9f9; border-top: 1px solid #eee; color: #777;">
                            <p style="margin: 0; font-size: 12px;">© 2025 <strong>Mi diario emocional</strong>. Todos los derechos reservados.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# --- 2. Estilo reutilizable para los Códigos ---
CODE_STYLE = "background-color: #f0f0f0; padding: 15px 20px; border-radius: 8px; font-size: 28px; text-align: center; letter-spacing: 3px; font-weight: bold; margin: 20px 0;"


# --- 3. Funciones de Correo Actualizadas ---

def send_password_reset_email(user_email: str, code: str):
    """Función para enviar el código de recuperación de contraseña."""
    
    subject = f"{code} es tu código para restablecer la contraseña en Mi diario emocional"
    
    # Mensaje de texto plano (para clientes de correo antiguos)
    message = (
        f"Hola,\n\n"
        f"Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.\n\n"
        f"Usa el siguiente código para completar el proceso:\n\n"
        f"Código de Verificación: {code}\n\n"
        f"Este código expirará en 5 minutos. Si no solicitaste esto, puedes ignorar este correo de forma segura.\n\n"
        f"Atentamente,\n"
        f"El equipo de Mi diario emocional"
    )
    
    # Contenido HTML para el correo
    html_content = (
        f'<h3 style="color: #333;">Hola,</h3>'
        f"<p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta para <strong>Mi diario emocional</strong>.</p>"
        f"<p>Usa el siguiente código para completar el proceso:</p>"
        f'<div style="{CODE_STYLE}">{code}</div>'
        f"<p style=\"font-size: 14px; color: #555;\">Este código expirará en 5 minutos. Si no solicitaste esto, puedes ignorar este correo de forma segura.</p>"
        f"<br>"
        f"<p>Atentamente,<br>El equipo de <strong>Mi diario emocional</strong></p>"
    )
    
    # Insertamos el contenido en la plantilla
    html_message = EMAIL_HTML_TEMPLATE.format(title="Restablecer Contraseña", content=html_content)

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
    
    subject = f"Confirmación de Cuenta Mi diario emocional - Código de Verificación"
    
    # Mensaje de texto plano (fallback)
    message = (
        f"Hola,\n\nGracias por registrarte en Mi diario emocional. "
        f"Tu código de verificación de cuenta es: {code}\n\n"
        f"Por favor, utilízalo en la aplicación para activar tu cuenta."
    )
    
    # Contenido HTML
    html_content = (
        f'<h3 style="color: #333;">¡Bienvenido a Mi diario emocional!</h3>'
        f"<p>Gracias por registrarte. Tu código de verificación de cuenta es:</p>"
        f'<div style="{CODE_STYLE}">{code}</div>'
        f"<p>Por favor, utilízalo en la aplicación para activar tu cuenta.</p>"
        f"<p>Este código expirará en 15 minutos.</p>"
        f"<br>"
        f"<p>Atentamente,<br>El equipo de <strong>Mi diario emocional</strong></p>"
    )
    
    # Insertamos el contenido en la plantilla
    html_message = EMAIL_HTML_TEMPLATE.format(title="Verifica tu Cuenta", content=html_content)

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
            html_message=html_message # <-- Añadimos la versión HTML
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo a {user_email}: {e}")
        return False


def send_verification_change_email(user_email: str, code: str):
    """Función para enviar el código de verificación por correo."""
    
    subject = f"{code} es tu código de verificación para Mi diario emocional"
    
    # Mensaje de texto plano (fallback)
    message = (
        f"Hola,\n\n"
        f"Hemos recibido una solicitud para cambiar el correo electrónico de tu cuenta a esta dirección.\n\n"
        f"Usa el siguiente código para confirmar el cambio:\n\n"
        f"Código de Verificación: {code}\n\n"
        f"Este código expirará en 5 minutos. Si no solicitaste este cambio, puedes ignorar este correo de forma segura.\n\n"
        f"Atentamente,\n"
        f"El equipo de Mi diario emocional"
    )
    
    # Contenido HTML
    html_content = (
        f'<h3 style="color: #333;">Hola,</h3>'
        f"<p>Hemos recibido una solicitud para cambiar el correo electrónico de tu cuenta en <strong>Mi diario emocional</strong> a esta dirección.</p>"
        f"<p>Usa el siguiente código para confirmar el cambio:</p>"
        f'<div style="{CODE_STYLE}">{code}</div>'
        f"<p style=\"font-size: 14px; color: #555;\">Este código expirará en 5 minutos. Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>"
        f"<br>"
        f"<p>Atentamente,<br>El equipo de <strong>Mi diario emocional</strong></p>"
    )
    
    # Insertamos el contenido en la plantilla
    html_message = EMAIL_HTML_TEMPLATE.format(title="Confirmar Cambio de Correo", content=html_content)

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
            html_message=html_message,
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
    
    subject = "¡Tu cuenta en Mi diario emocional ha sido aprobada!"
    
    # Mensaje de texto plano (fallback)
    message = (
        "Hola,\n\nNos complace informarte que tu cuenta de profesional ha sido validada y activada. "
        "Ya puedes iniciar sesión en la aplicación y comenzar a usar todas las herramientas.\n\n"
        "¡Bienvenido a Mi diario emocional!"
    )
    
    # Contenido HTML
    html_content = (
        f'<h3 style="color: #333;">¡Tu cuenta ha sido aprobada!</h3>'
        f"<p>Hola,</p>"
        f"<p>Nos complace informarte que tu cuenta de profesional ha sido validada y activada.</p>"
        f"<p>Ya puedes iniciar sesión en la aplicación y comenzar a usar todas las herramientas.</p>"
        f"<p>¡Bienvenido a <strong>Mi diario emocional</strong>!</p>"
    )
    
    # Insertamos el contenido en la plantilla
    html_message = EMAIL_HTML_TEMPLATE.format(title="Cuenta Aprobada", content=html_content)

    try:
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            [user_email],
            html_message=html_message # <-- Añadimos la versión HTML
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo de aprobación a {user_email}: {e}")
        return False


def send_rejection_email(user_email: str):
    """Envía un correo notificando que la cuenta ha sido rechazada."""
    
    subject = "Actualización sobre tu registro en Mi diario emocional"
    
    # Mensaje de texto plano (fallback)
    message = (
        "Hola,\n\nDespués de revisar tu solicitud de registro como profesional en Mi diario emocional, "
        "hemos encontrado inconsistencias y, por el momento, no ha sido aprobada.\n\n"
        "Si crees que esto es un error, por favor, ponte en contacto con nuestro equipo de soporte respondiendo a este correo.\n\n"
        "Lamentamos los inconvenientes."
    )
    
    # Contenido HTML
    html_content = (
        f'<h3 style="color: #333;">Actualización sobre tu registro</h3>'
        f"<p>Hola,</p>"
        f"<p>Después de revisar tu solicitud de registro como profesional en <strong>Mi diario emocional</strong>, "
        "hemos encontrado inconsistencias y, por el momento, no ha sido aprobada.</p>"
        f"<p>Si crees que esto es un error, por favor, ponte en contacto con nuestro equipo de soporte respondiendo a este correo.</p>"
        f"<br>"
        f"<p>Lamentamos los inconvenientes,<br>El equipo de <strong>Mi diario emocional</strong></p>"
    )
    
    # Insertamos el contenido en la plantilla
    html_message = EMAIL_HTML_TEMPLATE.format(title="Solicitud de Registro", content=html_content)
    
    try:
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            [user_email],
            html_message=html_message # <-- Añadimos la versión HTML
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo de rechazo a {user_email}: {e}")
        return False