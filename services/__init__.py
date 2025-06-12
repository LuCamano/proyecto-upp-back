from app.db import SessionDep
from sqlmodel import SQLModel, select
from models import Directivo, Establecimiento, Comuna, Estudiante, NivelPractica, Carrera, Tutor
from typing import Any, Dict

class BaseCrudService:
    def __init__(self, model: type[SQLModel]):
        self.model = model

    def create(self, session: SessionDep, obj: SQLModel):
        db_obj = self.model.model_validate(obj)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    
    def bulk_create(self, session: SessionDep, objs: list[SQLModel] | list[Dict[str, Any]]):
        if not objs:
            raise ValueError("No objects provided for bulk creation.")

        if isinstance(objs, list) and all(isinstance(obj, dict) for obj in objs):
            objs = [self.model.model_validate(obj) for obj in objs]

        session.bulk_save_objects(objs)
        session.commit()
        return {"message": "Bulk creation successful."}

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
    
    def delete_all(self, session: SessionDep):
        statement = select(self.model)
        objs = session.exec(statement).all()
        if not objs:
            raise ValueError(f"No {self.model.__name__} records found to delete.")
        
        for obj in objs:
            session.delete(obj)
        session.commit()
        return {"message": f"All {self.model.__name__} records deleted successfully."}
    
class DirectivoService(BaseCrudService):
    def __init__(self):
        super().__init__(Directivo)

    def bulk_create(self, session, objs):
        if not objs:
            raise ValueError("No objects provided for bulk creation.")
        
        for obj in objs:
            if isinstance(obj, dict):
                establecimiento_id = session.exec(select(Establecimiento).where(Establecimiento.nombre == obj.get('establecimiento'))).first()
                if not establecimiento_id:
                    raise ValueError(f"Establecimiento '{obj.get('establecimiento')}' not found.")
                obj['establecimiento_id'] = establecimiento_id.id
        db_objs = [Directivo.model_validate(obj) for obj in objs]
        session.bulk_save_objects(db_objs)
        session.commit()
        return {"message": "Bulk creation successful."}
    
class EstablecimientoService(BaseCrudService):
    def __init__(self):
        super().__init__(Establecimiento)
        
    def bulk_create(self, session, objs):
        if not objs:
            raise ValueError("No objects provided for bulk creation.")
        
        for obj in objs:
            if isinstance(obj, dict):
                comuna_id = session.exec(select(Comuna).where(Comuna.nombre == obj.get('comuna'))).first()
                if not comuna_id:
                    raise ValueError(f"Comuna '{obj.get('comuna')}' not found.")
                obj['comuna_id'] = comuna_id.id
        db_objs = [Establecimiento.model_validate(obj) for obj in objs]
        session.bulk_save_objects(db_objs)
        session.commit()
        return {"message": "Bulk creation successful."}
    
class NivelPracticaService(BaseCrudService):
    def __init__(self):
        super().__init__(NivelPractica)
        
    def bulk_create(self, session, objs):
        if not objs:
            raise ValueError("No objects provided for bulk creation.")
        
        for obj in objs:
            if isinstance(obj, dict):
                carrera_id = session.exec(select(Carrera).where(Carrera.nombre == obj.get('carrera'))).first()
                if not carrera_id:
                    raise ValueError(f"Carrera '{obj.get('carrera')}' not found.")
                obj['carrera_id'] = carrera_id.id
        db_objs = [NivelPractica.model_validate(obj) for obj in objs]
        session.bulk_save_objects(db_objs)
        session.commit()
        return {"message": "Bulk creation successful."}
    
class EstudianteService(BaseCrudService):
    def __init__(self):
        super().__init__(Estudiante)
        
    def bulk_create(self, session, objs):
        if not objs:
            raise ValueError("No objects provided for bulk creation.")
        
        for obj in objs:
            if isinstance(obj, dict):
                tutor_id = session.exec(select(Tutor).where(Tutor.nombre == obj.get('tutor'))).first()
                if tutor_id is not None:
                    obj['tutor_id'] = tutor_id.id
                carrera_id = session.exec(select(Carrera).where(Carrera.nombre == obj.get('carrera'))).first()
                if not carrera_id:
                    raise ValueError(f"Carrera '{obj.get('carrera')}' not found.")
                obj['carrera_id'] = carrera_id.id
                comuna_id = session.exec(select(Comuna).where(Comuna.nombre == obj.get('comuna'))).first()
                if not comuna_id:
                    raise ValueError(f"Comuna '{obj.get('comuna')}' not found.")
                obj['comuna_id'] = comuna_id.id
        db_objs = [Estudiante.model_validate(obj) for obj in objs]
        session.bulk_save_objects(db_objs)
        session.commit()
        return {"message": "Bulk creation successful."}