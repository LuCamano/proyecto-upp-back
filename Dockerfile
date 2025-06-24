# Usa una imagen oficial de Python como base
FROM python:3.13.5

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Establece las variables de entorno en el contenedor
ENV DATABASE_URL=""
ENV SMTP_USER=""
ENV SMTP_PASSWORD=""

# Expone el puerto en el que correrá la API (ajusta si usas otro puerto)
EXPOSE 8000

# Comando para ejecutar la API
CMD ["python", "run.py"]