from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..db import get_db
from ..models import Application, RiskScore
from ..schemas import ScoreOut
from ..services.calc import recalc_scores

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/recalc")
def recalc(db: Session = Depends(get_db)):
    n = recalc_scores(db)
    return {"recalculated_apps": n}

@router.get("/latest-scores", response_model=list[ScoreOut])
def latest_scores(db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    out = []
    for app in apps:
        s = (
            db.query(RiskScore)
            .filter(RiskScore.application_id == app.id)
            .order_by(desc(RiskScore.calculated_at))
            .first()
        )
        if s:
            out.append(s)
    out.sort(key=lambda x: x.score, reverse=True)
    return out
