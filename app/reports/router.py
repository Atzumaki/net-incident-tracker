from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.reports.model import Report
from app.reports.schemas import ReportCreate, ReportRead
from app.reports.service import create_report_with_grouping

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
async def create_report(
    data: ReportCreate,
    session: AsyncSession = Depends(get_session),
) -> Report:
    return await create_report_with_grouping(data, session)


@router.get("", response_model=list[ReportRead])
async def list_reports(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Report]:
    result = await session.scalars(
        select(Report).order_by(Report.created_at.desc()),
    )

    return result.all()


@router.get("/{report_id}", response_model=ReportRead)
async def get_report(
    report_id: int,
    session: AsyncSession = Depends(get_session),
) -> Report:
    report = await session.get(Report, report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return report