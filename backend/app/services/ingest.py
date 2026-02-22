from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Application, Finding

def get_or_create_app(db: Session, name: str) -> Application:
    app = db.query(Application).filter(Application.name == name).one_or_none()
    if app:
        return app
    app = Application(name=name, internet_exposed=False, data_sensitivity="low")
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def create_finding(db: Session, payload) -> Finding:
    app = get_or_create_app(db, payload.application_name)
    detected_at = payload.detected_at or datetime.utcnow()

    f = Finding(
        application_id=app.id,
        tool_source=payload.tool_source,
        tool_name=payload.tool_name,
        title=payload.title,
        normalized_type=payload.normalized_type,
        cwe=payload.cwe,
        severity=payload.severity,
        cvss=payload.cvss,
        exploit_available=payload.exploit_available,
        internet_exposed=payload.internet_exposed,
        status=payload.status,
        detected_at=detected_at,
        fixed_at=payload.fixed_at,
        external_id=payload.external_id,
        raw=payload.raw,
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return f
