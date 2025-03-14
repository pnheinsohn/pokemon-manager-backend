from datetime import datetime
from ninja import Schema
from django.shortcuts import get_object_or_404

from apps.reports.admin.router import router
from apps.reports.models import Report


class ReportSchema(Schema):
    id: int
    type: str
    status: str
    pending_at: datetime | None = None
    completed_at: datetime | None = None
    failed_at: datetime | None = None
    data: list

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }


@router.get("/{report_id}", response=ReportSchema)
def show_report(request, report_id: int):
    return get_object_or_404(Report, id=report_id)
