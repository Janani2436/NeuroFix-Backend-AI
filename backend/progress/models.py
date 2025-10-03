from django.db import models
from django.utils import timezone
from learning_plans.models import LearningPlan

class ProgressItem(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    learning_plan = models.ForeignKey(
        LearningPlan,
        on_delete=models.CASCADE,
        related_name='progress_items'
    )
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set the completion timestamp when status is changed to COMPLETED
        if self.status == self.Status.COMPLETED and self.completed_at is None:
            self.completed_at = timezone.now()
        # If status is changed from COMPLETED to something else, clear the timestamp
        elif self.status != self.Status.COMPLETED and self.completed_at is not None:
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} ({self.status})"