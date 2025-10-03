# learning_plans/permissions.py

from rest_framework import permissions
from .models import LearningPlan # Import the LearningPlan model

class IsPlanOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the plan's student owner or a superuser (admin) 
    to view/edit its nested ProgressItems.
    """

    def has_permission(self, request, view):
        # Authenticated users only
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Get the ID of the Learning Plan from the URL
        # We ASSUME 'learning_plan_pk' based on standard nested routing.
        plan_id = view.kwargs.get('learning_plan_pk') 
        
        if not plan_id:
            # If no plan ID is present in the URL (e.g., in a non-nested route), deny access.
            return False

        try:
            # Retrieve the LearningPlan object
            learning_plan = LearningPlan.objects.get(id=plan_id)
        except LearningPlan.DoesNotExist:
            # If the plan doesn't exist, we'll allow DRF to return a 404 later.
            return True 

        user = request.user
        
        # 1. Allow Superusers (Admins) to do anything
        if user.is_superuser:
            return True

        # 2. Allow the Student (Owner) to do anything
        if learning_plan.student == user:
            return True

        # DENY if none of the above conditions met
        return False