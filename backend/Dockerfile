FROM python:3.11-slim

# 1. Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev curl \
    libpango-1.0-0 libpangoft2-1.0-0 \
    libgobject-2.0-0 libcairo2 \
    libgdk-pixbuf-2.0-0 shared-mime-info \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 2. Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# 3. Directorio de trabajo
WORKDIR /app

# 4. ✅ Volver a la ruta completa
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Instalar modelo spaCy
RUN python -m spacy download es_core_news_md || echo "⚠️ spaCy download skipped"

# 6. ✅ Copiar desde backend/
COPY backend/ .

# 7. Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# 8. Exponer puerto
EXPOSE 8000

# 9. Comando de inicio con variable de entorno $PORT
CMD ["sh", "-c", "gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"]