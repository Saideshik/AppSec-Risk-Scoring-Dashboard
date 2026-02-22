from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Application
from ..schemas import AppCreate, AppOut

router = APIRouter(prefix="/apps", tags=["apps"])

@router.post("", response_model=AppOut)
def create_app(body: AppCreate, db: Session = Depends(get_db)):
    app = Application(**body.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("", response_model=list[AppOut])
def list_apps(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.name.asc()).all()
