## Antes de ejecutar el resto de la aplicación, es importante cargar las variables de entorno
USE_DOTENV = True
if USE_DOTENV:
    from dotenv import load_dotenv
    load_dotenv()

import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

from app import create_app


app = create_app()

if __name__ == "__main__":
    from uvicorn import run
    run(app, host="0.0.0.0", port=8000, log_level="info")