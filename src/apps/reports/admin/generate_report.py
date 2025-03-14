from datetime import datetime
from ninja import Schema
from django.utils import timezone

from apps.reports.admin.router import router
from apps.reports.models import Report
from apps.reports.tasks import generate_highest_level_pokemon_report, generate_most_common_base_pokemon_report


class GenerateReportResponseSchema(Schema):
    success: bool
    error: str | None = None


class GenerateReportPayloadSchema(Schema):
    report_type: str


@router.post("/", response={200: GenerateReportResponseSchema})
def generate_report(request, payload: GenerateReportPayloadSchema):
    report = Report.objects.create(
        type=payload.report_type,
        status="pending",
        pending_at=timezone.now(),
        data=[]
    )

    if payload.report_type == "level":
        generate_highest_level_pokemon_report.delay(report.id)
    elif payload.report_type == "common":
        generate_most_common_base_pokemon_report.delay(report.id)

    return GenerateReportResponseSchema(success=True)
