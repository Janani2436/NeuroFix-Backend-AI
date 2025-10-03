# progress/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# CORRECT IMPORTS for ProgressItemViewSet:
from .models import ProgressItem 
from .serializers import ProgressItemSerializer
# Import dependencies from the learning_plans app
from learning_plans.models import LearningPlan 
from learning_plans.permissions import IsPlanOwnerOrAdmin 


# ----------------------------------------------------------------------
# Progress Item ViewSet
# ----------------------------------------------------------------------

class ProgressItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, creating, and editing progress tasks 
    nested under a specific learning plan.
    """
    serializer_class = ProgressItemSerializer
    # APPLY THE SECURITY: Use the IsPlanOwnerOrAdmin permission
    permission_classes = [IsAuthenticated, IsPlanOwnerOrAdmin] 
    
    def get_queryset(self):
        """
        Filters ProgressItems to only show those belonging to the Learning Plan 
        specified in the URL keyword argument 'learning_plan_pk'.
        """
        # The IsPlanOwnerOrAdmin permission already ensured the user is allowed to access the plan.
        plan_id = self.kwargs.get('learning_plan_pk')
        if plan_id:
            return ProgressItem.objects.filter(learning_plan_id=plan_id).order_by('created_at')
        return ProgressItem.objects.none()

    def perform_create(self, serializer):
        """
        Saves the ProgressItem, associating it with the correct Learning Plan.
        """
        # Get the ID from the URL and associate the ProgressItem with the correct LearningPlan
        plan_id = self.kwargs.get('learning_plan_pk')
        learning_plan = LearningPlan.objects.get(pk=plan_id)
        serializer.save(learning_plan=learning_plan)