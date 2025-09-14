# learning_plans/views.py

from rest_framework import viewsets, permissions
from .models import LearningPlan
from .serializers import LearningPlanSerializer

class LearningPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows learning plans to be viewed or edited.
    """
    # ADD THIS LINE:
    queryset = LearningPlan.objects.all()
    
    serializer_class = LearningPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # The rest of this method stays exactly the same
        user = self.request.user
        if user.is_superuser:
            return LearningPlan.objects.all()
        if user.role == 'STUDENT':
            return LearningPlan.objects.filter(student=user)
        elif user.role in ['GUIDE', 'PARENT']:
            return LearningPlan.objects.all()
        return LearningPlan.objects.none()