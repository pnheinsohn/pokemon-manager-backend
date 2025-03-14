from ninja import Schema
from django.utils import timezone

from apps.reports.admin.router import router
from apps.reports.models import Report


class DeleteReportResponseSchema(Schema):
    success: bool


@router.delete("/{report_id}", response={200: DeleteReportResponseSchema})
def delete_report(request, report_id: int):
    Report.objects.get(id=report_id).delete()

    return DeleteReportResponseSchema(success=True)
