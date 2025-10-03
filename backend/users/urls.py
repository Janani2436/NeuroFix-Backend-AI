# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Import the necessary views from the installed library
from django_rest_passwordreset.views import (
    ResetPasswordRequestTokenViewSet,
    ResetPasswordConfirmViewSet,
)
from .views import RegisterView, CurrentUserView # Assuming you have these views

urlpatterns = [
    # Existing Auth routes
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),

    # ----------------------------------------
    # NEW PASSWORD RESET ROUTES
    # ----------------------------------------
    
    # 1. POST /api/password-reset/ (Takes email, sends/prints reset token)
    path(
        'password-reset/', 
        ResetPasswordRequestTokenViewSet.as_view({'post': 'create'}), 
        name='password_reset_request'
    ),
    
    # 2. POST /api/password-reset-confirm/ (Takes token, new password, and confirms reset)
    path(
        'password-reset-confirm/', 
        ResetPasswordConfirmViewSet.as_view({'post': 'create'}), 
        name='password_reset_confirm'
    ),
]