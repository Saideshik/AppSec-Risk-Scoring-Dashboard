from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Application, Finding, RiskScore
from ..scoring import compute_app_risk, compute_mttr_days

def recalc_scores(db: Session) -> int:
    apps = db.query(Application).all()
    count = 0

    for app in apps:
        open_findings = (
            db.query(Finding)
            .filter(Finding.application_id == app.id, Finding.status == "open")
            .all()
        )
        fixed_findings = (
            db.query(Finding)
            .filter(Finding.application_id == app.id, Finding.status == "fixed")
            .all()
        )

        result = compute_app_risk(app, open_findings)
        mttr = compute_mttr_days(fixed_findings)

        score = RiskScore(
            application_id=app.id,
            score=result["score"],
            label=result["label"],
            calculated_at=datetime.utcnow(),
            open_critical=result["open_counts"]["critical"],
            open_high=result["open_counts"]["high"],
            open_medium=result["open_counts"]["medium"],
            open_low=result["open_counts"]["low"],
            mttr_days=mttr,
        )
        db.add(score)
        count += 1

    db.commit()
    return count
