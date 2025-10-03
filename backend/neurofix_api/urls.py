# neurofix_api/urls.py

from django.contrib import admin
from django.urls import path, include

# Import the necessary documentation views (SpectacularAPIView is the schema)
# We only need the primary views for the Swagger and Redoc UIs
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)

urlpatterns = [
    # ----------------------------------------
    # API Documentation Routes
    # ----------------------------------------
    # 1. Schema generation route (used by the UIs)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI route (Interactive Documentation)
    path(
        'api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), 
        name='swagger-ui'
    ),
    
    # 3. Redoc UI route (Alternative Documentation View)
    path(
        'api/schema/redoc/', 
        SpectacularRedocView.as_view(url_name='schema'), 
        name='redoc'
    ),
    
    # ----------------------------------------
    # Core API Routes
    # ----------------------------------------
    path('admin/', admin.site.urls),
    # Includes Auth and Password Reset routes
    path('api/', include('users.urls')), 
    # Includes Learning Plan, nested Progress, and the AI Suggestion route
    path('api/', include('learning_plans.urls')), 
]
