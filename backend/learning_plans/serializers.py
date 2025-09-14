from rest_framework import serializers
from .models import LearningPlan

class LearningPlanSerializer(serializers.ModelSerializer):
    # To show the student's username in the API response instead of just their ID
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = LearningPlan
        # We list 'student' for writing, and 'student_username' for reading
        fields = ['id', 'student', 'student_username', 'title', 'description', 'created_at', 'modified_at']
        # The 'student' field is for creating/updating a plan (providing the student's ID)
        extra_kwargs = {'student': {'write_only': True}}