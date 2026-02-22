from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import FindingIn, FindingOut
from ..services.ingest import create_finding

router = APIRouter(prefix="/findings", tags=["findings"])

@router.post("", response_model=FindingOut)
def ingest_finding(body: FindingIn, db: Session = Depends(get_db)):
    f = create_finding(db, body)
    return f
