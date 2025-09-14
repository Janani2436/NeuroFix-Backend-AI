from django.db import models
# We need to import BOTH CustomUser and Role from users.models
from users.models import CustomUser, Role

class LearningPlan(models.Model):
    # Link to a student. Ensures only users with the 'STUDENT' role can be assigned.
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='learning_plans',
        # Use the direct reference to Role, not through CustomUser
        limit_choices_to={'role': Role.STUDENT}
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # We also update this to use email, since username is no longer guaranteed
        return f"{self.title} for {self.student.email}"