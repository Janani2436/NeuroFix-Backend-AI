# learning_plans/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import LearningPlanViewSet
from progress.views import ProgressItemViewSet # Import the nested ViewSet

# 1. Main Router
# The default base name for LearningPlanViewSet will be 'learningplan'
router = routers.DefaultRouter()
router.register(r'learning-plans', LearningPlanViewSet)

# 2. Nested Router
# The parent lookup keyword 'learning_plan_pk' MUST match the name used in the 
# ProgressItemViewSet.get_queryset() and IsPlanOwnerOrAdmin.has_permission()
learning_plans_router = routers.NestedSimpleRouter(
    router, r'learning-plans', lookup='learning_plan'
)

# 3. Register the Progress Items as nested under Learning Plans
# The base URL will be: /api/learning-plans/{learning_plan_pk}/progress
# The nested lookup is automatically set to 'learning_plan_pk'
learning_plans_router.register(
    r'progress', ProgressItemViewSet, basename='plan-progress'
)

urlpatterns = [
    # Main learning plan routes: /api/learning-plans/
    path('', include(router.urls)),
    # Nested progress routes: /api/learning-plans/{id}/progress/
    path('', include(learning_plans_router.urls)), 
]