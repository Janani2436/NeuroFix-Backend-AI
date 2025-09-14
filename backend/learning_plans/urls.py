from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningPlanViewSet

router = DefaultRouter()
router.register(r'', LearningPlanViewSet, basename='learningplan')

urlpatterns = [
    path('', include(router.urls)),
]