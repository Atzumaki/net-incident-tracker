from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.incidents.model import Incident, IncidentStatus
from app.reports.model import Report
from app.reports.schemas import ReportCreate

ACTIVE_INCIDENT_STATUSES = (
    IncidentStatus.OPEN,
    IncidentStatus.IN_PROGRESS,
)


def normalize_address(address: str) -> str:
    return " ".join(address.casefold().split())


async def create_report_with_grouping(
    data: ReportCreate,
    session: AsyncSession,
) -> Report:
    normalized_address = normalize_address(data.address)

    incident = await session.scalar(
        select(Incident)
        .where(
            Incident.normalized_address == normalized_address,
            Incident.issue_type == data.issue_type,
            Incident.status.in_(ACTIVE_INCIDENT_STATUSES),
        )
        .order_by(Incident.created_at.desc())
        .limit(1),
    )

    if incident is None:
        incident = Incident(
            address=data.address.strip(),
            normalized_address=normalized_address,
            issue_type=data.issue_type,
        )
        session.add(incident)
        await session.flush()

    report_data = data.model_dump()
    report_data["address"] = data.address.strip()

    report = Report(
        **report_data,
        incident_id=incident.id,
    )

    session.add(report)
    incident.reports_count += 1

    await session.commit()
    await session.refresh(report)

    return report