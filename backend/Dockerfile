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

# 4. Copiar requirements.txt PRIMERO (desde la carpeta backend)
COPY ./requirements.txt .

# 5. Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Instalar modelo spaCy (no crítico)
RUN python -m spacy download es_core_news_md || echo "⚠️  spaCy download skipped"

# 7. Copiar todo el código del backend
COPY . .

# 8. Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# 9. Exponer puerto
EXPOSE 8000

# 10. Comando de inicio
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]