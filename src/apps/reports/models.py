from django.db import models
from django.db.models import TextChoices

class Report(models.Model):
    """Manages Pokemon-related reports and their generation status.

    This model handles different types of reports about Pokemon data,
    tracking their generation status and storing the results. It supports
    multiple report types and maintains timing information for the
    report generation process.

    Attributes:
        pending_at (DateTimeField): When the report was requested
        completed_at (DateTimeField): When the report finished successfully
        failed_at (DateTimeField): When the report failed, if applicable
        type (str): Type of report ('common' or 'level')
        status (str): Current status (PENDING, COMPLETED, or FAILED)
        data (JSONField): The actual report data in JSON format

    Report Types:
        common: Shows the most common Pokemon in the system
        level: Shows Pokemon sorted by their level
    """
    class Status(TextChoices):
        """Available statuses for report generation.

        Choices:
            PENDING: Report has been requested but not generated
            COMPLETED: Report has been successfully generated
            FAILED: Report generation failed
        """
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    pending_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    failed_at = models.DateTimeField(null=True)

    type = models.CharField(max_length=20, choices=[
        ('common', 'Most Common'),
        ('level', 'Highest Level')
    ])
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    data = models.JSONField(default=list)

    class Meta:
        indexes = [models.Index(fields=['type', 'status'])]
        ordering = ['-pending_at']

    def __str__(self):
        if self.status == self.Status.PENDING:
            return f"Report {self.type} (pending at {self.pending_at})"
        elif self.status == self.Status.COMPLETED:
            return f"Report {self.type} (completed at {self.completed_at})"
        elif self.status == self.Status.FAILED:
            return f"Report {self.type} (failed at {self.failed_at})"
