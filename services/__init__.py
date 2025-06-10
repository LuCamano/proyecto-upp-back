from app.db import SessionDep
from sqlmodel import SQLModel, select
from models import Directivo, DirectivoEstablecimiento, DirectivoEstablecimientoBase

class BaseCrudService:
    def __init__(self, model: type[SQLModel]):
        self.model = model

    def create(self, session: SessionDep, obj: SQLModel):
        db_obj = self.model.model_validate(obj)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    
    def all(self, session: SessionDep):
        statement = select(self.model)
        results = session.exec(statement).all()
        return results
    
    def read(self, session: SessionDep, obj_id):
        obj = session.get(self.model, obj_id)
        if not obj:
            raise ValueError(f"{self.model.__name__} not found with ID {obj_id}")
        return obj
    
    def update(self, session: SessionDep, obj_id, obj_data: SQLModel):
        obj = session.get(self.model, obj_id)
        if not obj:
            raise ValueError(f"{self.model.__name__} not found with ID {obj_id}")
        
        for key, value in obj_data.model_dump().items():
            setattr(obj, key, value)
        
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    
    def delete(self, session: SessionDep, obj_id):
        obj = session.get(self.model, obj_id)
        if not obj:
            raise ValueError(f"{self.model.__name__} not found with ID {obj_id}")
        
        session.delete(obj)
        session.commit()
        return {"message": f"{self.model.__name__} with ID {obj_id} deleted successfully"}
    
class DirectivoService(BaseCrudService):
    def __init__(self):
        super().__init__(Directivo)
        
    def create(self, session: SessionDep, obj, establecimiento_id: str):
        directivo = super().create(session, obj)
        if establecimiento_id:
            directivo_establecimiento = DirectivoEstablecimientoBase(
                directivo_id=directivo.id,
                establecimiento_id=establecimiento_id
            )
            db_DE = DirectivoEstablecimiento.model_validate(directivo_establecimiento)
            session.add(db_DE)
            session.commit()
            session.refresh(db_DE)
        return directivo