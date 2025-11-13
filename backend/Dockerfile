FROM python:3.11-slim

WORKDIR /app

# Copiar requirements PRIMERO para mejor cache
COPY requirements.txt .

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y \
    gcc libpq-dev \
    libpango-1.0-0 libpangoft2-1.0-0 \
    libgobject-2.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Instalar spaCy
RUN python -m spacy download es_core_news_md || true

# Copiar aplicación
COPY . .

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]