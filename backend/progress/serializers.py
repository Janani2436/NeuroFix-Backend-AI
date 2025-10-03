from rest_framework import serializers
from .models import ProgressItem

class ProgressItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressItem
        # The learning_plan will be set from the URL, so we make it read-only here
        fields = ['id', 'learning_plan', 'description', 'status', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['learning_plan']