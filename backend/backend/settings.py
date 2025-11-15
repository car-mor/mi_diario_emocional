"""
Django settings for backend project.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# Límite de tamaño de archivo para uploads (50MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB en bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB en bytes

# Tamaño máximo del body de la request (importante para archivos grandes)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://midiarioemocional-production.up.railway.app",
    "https://*.railway.app",  # Permite cualquier subdominio de Railway
]
# Application definition

INSTALLED_APPS = [
    # Apps por defecto de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Soporte de postgreSQL
    "django.contrib.postgres",
    # Apps de Terceros (Django REST Framework y JWT)
    "rest_framework",
    "rest_framework_simplejwt",
    # Aplicaciones creadas
    "users",
    "diary",
    "reports",
    "api",
    "corsheaders",
    "anymail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config(
            "DB_HOST", default="localhost"
        ),  # Opcional: define un valor por defecto si la variable no existe
        "PORT": config("DB_PORT", default="5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # Esto permite la autenticación basada en tokens JWT (Access Token)
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # Si usas sesiones para el Admin de Django o pruebas
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        # Opcional: Esto bloquea el acceso por defecto a todos, tienes que abrirlo explícitamente
        # 'rest_framework.permissions.IsAuthenticated',
        # Puedes mantenerlo más abierto y controlar la seguridad en cada vista
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),  # El token de acceso dura 10 minutos
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # El token de refresco dura 1 día
    "ROTATE_REFRESH_TOKENS": True,  # Rotar el token de refresco al usarlo para mayor seguridad
    "BLACKLIST_AFTER_ROTATION": True,  # Poner en lista negra el token de refresco anterior
    # Configuración de Algoritmo (usualmente se deja así)
    "ALGORITHM": "HS256",
    # Es importante que use la SECRET_KEY de tu proyecto para firmar los tokens
    "SIGNING_KEY": config("DJANGO_SECRET_KEY"),
}

EMAIL_BACKEND = config("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")
ANYMAIL_BREVO_API_KEY = config("ANYMAIL_BREVO_API_KEY")

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:5173").split(",")
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

AUTH_USER_MODEL = "users.User"

# Configuración de Archivos de Medios
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")
