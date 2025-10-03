# learning_plans/models.py

from django.db import models
from users.models import CustomUser, Role # We need to import BOTH CustomUser and Role

class LearningPlan(models.Model):
    # Link to a student. Ensures only users with the 'STUDENT' role can be assigned.
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='learning_plans',
        # Restrict choices to users with the STUDENT role
        limit_choices_to={'role': Role.STUDENT}
    )
    
    # NEW FIELD: Link to a guide (GUIDE role). This field is optional.
    guide = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  # If the guide is deleted, plan remains but guide field is set to null
        null=True,
        blank=True,
        related_name='guided_plans',
        # Restrict choices to users with the GUIDE role
        limit_choices_to={'role': Role.GUIDE}
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Updated to include the guide's email if available
        guide_email = f" (Guide: {self.guide.email})" if self.guide else ""
        return f"{self.title} for {self.student.email}{guide_email}"