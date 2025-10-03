# neurofix_api/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv # <-- NEW IMPORT

# Load environment variables from .env file
load_dotenv() # <-- NEW CALL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-9ytolci+&jm@@@af8%+iwd6@atlt6jf(1soc3=e_7cwm66se*q'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    '172.168.64.148', 
    '1e788b17c486.ngrok-free.app'
]

# Application definition

INSTALLED_APPS = [
    'users',
    'learning_plans',
    'progress',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_rest_passwordreset',
    'drf_spectacular',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'neurofix_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # ADDED debug processor
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'neurofix_api.wsgi.application'

# Database (Your existing PostgreSQL configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neurofix_db',
        'USER': 'postgres',
        'PASSWORD': 'Plusestenvous@06', 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- Email Configuration (for Password Reset) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
PASSWORD_RESET_CONFIRM_URL = 'password-reset-confirm/{uid}/{token}'
DEFAULT_FROM_EMAIL = 'support@neurofix.com'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Custom Project Settings ---

# Gemini API Key (Securely loaded from the .env file)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '') # <-- SECURE KEY LOADING

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # Required for spectacular
}

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# CORS Settings (Your existing settings)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 
    'http://localhost:8080',
]

# DRF SPECTACULAR SETTINGS
SPECTACULAR_SETTINGS = {
    'TITLE': 'NeuroFix Backend API',
    'DESCRIPTION': 'REST API for the NeuroFix neuro-adaptive learning platform, supporting students with disabilities. Focused on personalized learning plans and multimodal access.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, 
}