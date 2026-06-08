from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.incidents.model import IncidentStatus
from app.reports.model import IssueType


class IncidentRead(BaseModel):
    id: int
    address: str
    normalized_address: str
    issue_type: IssueType
    status: IncidentStatus
    reports_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus