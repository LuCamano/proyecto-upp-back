# Usa una imagen oficial de Python como base
FROM python:3.13.5

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_CL.UTF-8/es_CL.UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Establece las variables de entorno en el contenedor
ENV LANG=es_CL.UTF-8
ENV LC_TIME=es_CL.UTF-8
ENV TZ=America/Santiago
ENV DATABASE_URL=""
ENV SMTP_USER=""
ENV SMTP_PASSWORD=""

# Expone el puerto en el que correrá la API (ajusta si usas otro puerto)
EXPOSE 8000

# Comando para ejecutar la API
CMD ["python", "run.py"]