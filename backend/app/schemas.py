from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

Severity = Literal["critical", "high", "medium", "low", "info"]
ToolSource = Literal["SAST", "DAST", "SCA", "CONTAINER", "CLOUD", "RUNTIME"]
Status = Literal["open", "fixed", "accepted"]

class AppCreate(BaseModel):
    name: str
    owner: Optional[str] = None
    internet_exposed: bool = False
    data_sensitivity: Literal["low", "medium", "high"] = "low"

class AppOut(BaseModel):
    id: int
    name: str
    owner: Optional[str]
    internet_exposed: bool
    data_sensitivity: str
    created_at: datetime

    class Config:
        from_attributes = True

class FindingIn(BaseModel):
    application_name: str = Field(..., description="App name, will be created if missing")
    tool_source: ToolSource
    tool_name: Optional[str] = None
    title: str
    normalized_type: Optional[str] = None
    cwe: Optional[str] = None
    severity: Severity
    cvss: Optional[float] = None
    exploit_available: bool = False
    internet_exposed: bool = False
    status: Status = "open"
    detected_at: Optional[datetime] = None
    fixed_at: Optional[datetime] = None
    external_id: Optional[str] = None
    raw: Optional[str] = None

class FindingOut(BaseModel):
    id: int
    application_id: int
    tool_source: str
    tool_name: Optional[str]
    title: str
    severity: str
    cvss: Optional[float]
    exploit_available: bool
    internet_exposed: bool
    status: str
    detected_at: datetime
    fixed_at: Optional[datetime]

    class Config:
        from_attributes = True

class ScoreOut(BaseModel):
    application_id: int
    score: int
    label: str
    calculated_at: datetime
    open_critical: int
    open_high: int
    open_medium: int
    open_low: int
    mttr_days: Optional[float]

    class Config:
        from_attributes = True
