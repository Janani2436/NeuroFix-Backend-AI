from django.contrib import admin
from django.urls import path, include

# Import our new custom view
from users.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('users.urls')),

    # Use our custom view for the main token endpoint
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # The refresh token view can stay the same
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/learning-plans/', include('learning_plans.urls')),
]