# --- ETAPA 1: EL CONSTRUCTOR (BUILDER) ---
FROM python:3.11 AS builder

WORKDIR /app

# 1. Instala dependencias de CONSTRUCCIÓN
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

# 3. ✅ INSTALA PYTORCH CPU PRIMERO (SEPARADO)
RUN pip install --no-cache-dir torch==2.1.2+cpu --index-url https://download.pytorch.org/whl/cpu

# 4. Copia requirements.txt SIN torch
COPY backend/requirements.txt .

# 5. Instala el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 6. Instala spaCy
RUN python -m spacy download es_core_news_md

# 7. Copia código
COPY backend/ .


# --- ETAPA 2: LA IMAGEN FINAL (SLIM) ---
FROM python:3.11-slim

WORKDIR /app

# 1. Solo dependencias de RUNTIME
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
COPY --from=builder /app /app

# 4. Variables de entorno
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 5. Comando de inicio
CMD ["sh", "-c", "gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"]