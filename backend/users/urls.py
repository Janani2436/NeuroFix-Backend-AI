from django.urls import path
# Import the new RegisterView
from .views import UserListView, CurrentUserView, RegisterView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    # Add this new URL for registration
    path('register/', RegisterView.as_view(), name='register'),
]