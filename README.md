# Guía de Desarrollo

## Requisitos Previos
- Python 3.10 o superior
- Entorno virtual (recomendado)
- Servidor PostgreSQL configurado y accesible

## Instalación
1. Clonar el repositorio.
2. Crear y activar un entorno virtual:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```
     python -m venv venv
     source venv/bin/activate
     ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Configurar la variable `DATABASE_URL` en el archivo `.env`.

## Ejecución
1. Ejecutar la aplicación:
   ```
   python run.py
   ```
2. La API se servirá por defecto en `http://0.0.0.0:8000`.

## Contribuir
- Crear una rama nueva.
- Realizar cambios y pruebas.
- Enviar un Pull Request con una descripción clara.
