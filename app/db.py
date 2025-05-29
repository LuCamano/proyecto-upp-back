import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url, echo=True) # Desactivar el echo para producción

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]