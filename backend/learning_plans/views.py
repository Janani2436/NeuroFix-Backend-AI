# learning_plans/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# CORRECT IMPORTS for LearningPlanViewSet:
from .models import LearningPlan 
from .serializers import LearningPlanSerializer
from .permissions import IsPlanOwnerOrAdmin 
from .ai_services import generate_next_task_suggestion # IMPORT NEW AI SERVICE

# ----------------------------------------------------------------------
# Learning Plan ViewSet
# ----------------------------------------------------------------------

class LearningPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows learning plans to be viewed or edited.
    Controls access based on user role: Admin, Student, or Guide.
    """
    queryset = LearningPlan.objects.all() 
    serializer_class = LearningPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the LearningPlan queryset based on the authenticated user's role.
        """
        user = self.request.user
        
        if user.is_superuser:
            # 1. ADMINS see everything
            return LearningPlan.objects.all()
        
        elif user.role == 'STUDENT':
            # 2. STUDENTS see only their own plans
            return LearningPlan.objects.filter(student=user)
            
        elif user.role == 'GUIDE':
            # 3. GUIDES see only the plans they are assigned to
            return LearningPlan.objects.filter(guide=user)
            
        # Default: If the user role is not explicitly handled or defined, deny access.
        return LearningPlan.objects.none()

    @action(detail=True, methods=['get'], url_path='suggest-task')
    def suggest_task(self, request, pk=None):
        """
        Custom action to call the AI service and generate the next best task suggestion 
        for the given Learning Plan.
        
        URL: /api/learning-plans/{pk}/suggest-task/
        """
        try:
            # Ensure the user has permission to view this plan
            plan = self.get_object() 
        except Exception:
            return Response(
                {"detail": "Not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Call the AI service function
        suggestion_data = generate_next_task_suggestion(plan.pk)

        if "error" in suggestion_data:
            return Response(
                {"detail": suggestion_data["error"]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(suggestion_data, status=status.HTTP_200_OK)
