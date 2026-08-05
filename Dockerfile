FROM python:3.11-slim

# Evitar creación de bytecode (.pyc) y habilitar buffer de salida en tiempo real para logs en Coolify
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas por Pillow y librerías gráficas
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python (optimizando la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente del proyecto
COPY . .

# Seguridad: Crear y cambiar a un usuario sin privilegios root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer los puertos que utilizan Streamlit y FastAPI
EXPOSE 8501 8001

# Comando por defecto (será sobrescrito en el docker-compose por cada servicio)
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
