from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class IssueType(StrEnum):
    NO_INTERNET = "no_internet"
    LOW_SPEED = "low_speed"
    UNSTABLE_CONNECTION = "unstable_connection"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255), index=True)
    issue_type: Mapped[IssueType] = mapped_column(Enum(IssueType), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )