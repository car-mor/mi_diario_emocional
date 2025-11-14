# --- ETAPA 1: EL CONSTRUCTOR (BUILDER) ---
FROM python:3.11 AS builder

WORKDIR /app

# 1. Instala dependencias de CONSTRUCCIÓN
# (Mantenemos pango/cairo para WeasyPrint, tal como acordamos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    pkg-config \
    libpango-1.0-0 libpangoft2-1.0-0 \
    libgobject-2.0-0 libcairo2 \
    libgdk-pixbuf-2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# 2. Crea virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Copia tu NUEVO requirements.txt (el ligero)
COPY backend/requirements.txt .

# 4. Instala el resto de dependencias (ahora mucho más rápido)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia código de tu app
COPY backend/ .

# 6. +++ AÑADIDO +++
# ¡Este es el paso clave para arreglar tu panel de admin!
# Ejecuta collectstatic para que WhiteNoise encuentre el CSS.
RUN python manage.py collectstatic --noinput

# --- ETAPA 2: LA IMAGEN FINAL (SLIM) ---
FROM python:3.11-slim

WORKDIR /app

# 1. Solo dependencias de RUNTIME
# (libpq5 para postgres, pango/cairo para WeasyPrint)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libpango-1.0-0 libpangoft2-1.0-0 \
    libgobject-2.0-0 libcairo2 \
    libgdk-pixbuf-2.0-0 \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# 2. Copia VENV desde builder
COPY --from=builder /opt/venv /opt/venv

# 3. Copia código desde builder
# Esto AHORA INCLUYE la carpeta 'staticfiles' que creamos arriba
COPY --from=builder /app /app

# 4. Variables de entorno
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 5. Comando de inicio (Este se queda igual)
# collectstatic ya se hizo en el build, aquí solo corremos el server
CMD ["sh", "-c", "gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"]