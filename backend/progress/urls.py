from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgressItemViewSet

router = DefaultRouter()
router.register(r'', ProgressItemViewSet, basename='progressitem')

urlpatterns = [
    path('', include(router.urls)),
]