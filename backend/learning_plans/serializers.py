# learning_plans/serializers.py

from rest_framework import serializers
from .models import LearningPlan

class LearningPlanSerializer(serializers.ModelSerializer):
    
    # 1. Student Email (Read-only field for display, replacing the incorrect 'username' assumption)
    student_email = serializers.CharField(source='student.email', read_only=True)
    
    # 2. NEW FIELD: Guide Email (Read-only field for display)
    guide_email = serializers.CharField(source='guide.email', read_only=True, required=False)

    class Meta:
        model = LearningPlan
        # We list all fields, including the new 'guide' and the display fields
        fields = [
            'id', 
            'student', 
            'student_email', 
            'guide',            # For writing/inputting the guide's ID
            'guide_email',      # For reading/displaying the guide's email
            'title', 
            'description', 
            'created_at', 
            'modified_at'
        ]
        
        # Configure the writable fields to be write-only for cleaner API input/output
        extra_kwargs = {
            'student': {'write_only': True},
            'guide': {'write_only': True, 'required': False}, # Guide is optional when creating/updating
        }
        
        # Ensure read-only fields are protected
        read_only_fields = ['created_at', 'modified_at']