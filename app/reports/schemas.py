from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.reports.model import IssueType


class ReportCreate(BaseModel):
    address: str = Field(min_length=5, max_length=255)
    issue_type: IssueType
    description: str | None = Field(default=None, max_length=1000)


class ReportRead(BaseModel):
    id: int
    address: str
    issue_type: IssueType
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)