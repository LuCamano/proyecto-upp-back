from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.email_routes import router as email_router
from contextlib import asynccontextmanager
from routes import router
from .db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    create_db_and_tables()
    yield
    # Code to run at shutdown

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    # Register routers
        # CORS para que React pueda llamar
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # puedes restringir a tu frontend después
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api/v1", tags=["api"])
    
    return app