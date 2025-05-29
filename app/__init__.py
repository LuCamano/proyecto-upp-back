from fastapi import FastAPI
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
    app.include_router(router, prefix="/api/v1", tags=["api"])
    
    return app