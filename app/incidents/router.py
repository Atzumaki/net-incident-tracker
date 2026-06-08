from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.incidents.model import Incident
from app.incidents.schemas import IncidentRead, IncidentStatusUpdate

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentRead])
async def list_incidents(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Incident]:
    result = await session.scalars(
        select(Incident).order_by(Incident.updated_at.desc()),
    )

    return result.all()


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(
    incident_id: int,
    session: AsyncSession = Depends(get_session),
) -> Incident:
    incident = await session.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident


@router.patch("/{incident_id}/status", response_model=IncidentRead)
async def update_incident_status(
    incident_id: int,
    data: IncidentStatusUpdate,
    session: AsyncSession = Depends(get_session),
) -> Incident:
    incident = await session.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    incident.status = data.status

    await session.commit()
    await session.refresh(incident)

    return incident