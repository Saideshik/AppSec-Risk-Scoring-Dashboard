from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    owner = Column(String(200), nullable=True)
    internet_exposed = Column(Boolean, default=False, nullable=False)
    data_sensitivity = Column(String(20), default="low", nullable=False)  # low/medium/high
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    findings = relationship("Finding", back_populates="application", cascade="all, delete-orphan")
    scores = relationship("RiskScore", back_populates="application", cascade="all, delete-orphan")

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)

    tool_source = Column(String(50), nullable=False)   # SAST/DAST/SCA/CONTAINER/CLOUD/RUNTIME
    tool_name = Column(String(120), nullable=True)

    title = Column(String(300), nullable=False)
    normalized_type = Column(String(120), nullable=True)
    cwe = Column(String(50), nullable=True)

    severity = Column(String(20), nullable=False)  # critical/high/medium/low/info
    cvss = Column(Float, nullable=True)

    exploit_available = Column(Boolean, default=False, nullable=False)
    internet_exposed = Column(Boolean, default=False, nullable=False)  # per finding override

    status = Column(String(20), default="open", nullable=False)  # open/fixed/accepted
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    fixed_at = Column(DateTime, nullable=True)

    external_id = Column(String(200), nullable=True)
    raw = Column(Text, nullable=True)

    application = relationship("Application", back_populates="findings")

Index("ix_findings_app_status", Finding.application_id, Finding.status)

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    score = Column(Integer, nullable=False)  # 0-100
    label = Column(String(20), nullable=False)  # Low/Med/High/Critical
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    open_critical = Column(Integer, default=0, nullable=False)
    open_high = Column(Integer, default=0, nullable=False)
    open_medium = Column(Integer, default=0, nullable=False)
    open_low = Column(Integer, default=0, nullable=False)
    mttr_days = Column(Float, nullable=True)

    application = relationship("Application", back_populates="scores")

Index("ix_scores_app_time", RiskScore.application_id, RiskScore.calculated_at)
