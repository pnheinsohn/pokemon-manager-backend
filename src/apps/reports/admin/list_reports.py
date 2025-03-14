from typing import List, Optional
from datetime import datetime

from ninja import FilterSchema, Query, Schema
from ninja.pagination import paginate
from pydantic import Field

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


class ReportFilterSchema(FilterSchema):
    id: Optional[int] = None
    status: Optional[str] = Field(None, q="status__iexact")
    pending_at: Optional[datetime] = Field(None, q="pending_at__gte", serialization_alias="pendingAt")
    completed_at: Optional[datetime] = Field(None, q="completed_at__gte", serialization_alias="completedAt")
    failed_at: Optional[datetime] = Field(None, q="failed_at__gte", serialization_alias="failedAt")
    data: Optional[list] = Field(default_factory=list)

    def get_filter_expression(self):
        # Don't include empty data filter
        if not self.data:
            self.data = None
        return super().get_filter_expression()

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }


@router.get("/", response={200: List[ReportSchema]})
@paginate
def list_reports(request, report_type: str, filters: ReportFilterSchema = Query(...)):
    return Report.objects.filter(type=report_type).filter(filters.get_filter_expression())
