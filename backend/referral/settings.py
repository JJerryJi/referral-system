"""
Django settings for referral project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import json 
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import redis
from pathlib import Path
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d5g)w@ugg7&%5&agl(*)_bx!5-gr$l8no+1=hyj19sp(^kkq_f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# define customized user model here
AUTH_USER_MODEL = 'user.User'

# Application definition

INSTALLED_APPS = [
    'user',
    'job_post', 
    'application',
    'corsheaders',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
]



CORS_ALLOW_ALL_ORIGINS = True 

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "referral.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "referral.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "referral_system",       # Your PostgreSQL database name
        "USER": "referral_user",         # Your PostgreSQL username
        "PASSWORD": "jerry",          # Your PostgreSQL password
        "HOST": "localhost",            # Host where your PostgreSQL server is running
        "PORT": "5432",                     # Leave empty to use the default PostgreSQL port (5432)
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",  # Add your frontend URL here
]

CORS_ALLOW_HEADERS = [
    "access-control-allow-headers",
    "access-control-allow-methods",
    "access-control-allow-origin",
    "content-type", 
    "Authorization",
    "token"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',  # Add 'OPTIONS' to the list of allowed methods
    'PATCH',
    'POST',
    'PUT',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Path to your media folder
print(MEDIA_ROOT)

REDIS_HOST = 'localhost'  # Redis server address
REDIS_PORT = 6379  # Redis server port
REDIS_DB = 0  # Redis database number

# Cache settings using Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',  # Redis server address and database number
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Token expiration time
TOKEN_EXPIRATION = timedelta(days=3)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (  #If there is rest_ The framework configuration item can be added separately
        'referral.settings.RedisTokenAuthentication',  # Project name. File where the recertification class is located. Class name
    ),
}

# score board config:
CLICK_SCORE = 1
FAVORITE_SCORE = 5
APPLY_SCORE = 10

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=0)

class RedisTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        user_id_bytes = REDIS_CLIENT.get(key)
        if user_id_bytes:
            user_id = int(user_id_bytes)  # Convert the string to an integer
            # print(user_id)

            # Create a user object with the user ID
            user = get_user_model().objects.filter(id=user_id).first()
            if user and user.is_active:
                return (user, None)  # Returning the user

        # Handle the case when the user_id is not found in Redis or the user is not active
        raise exceptions.AuthenticationFailed(_('Invalid token.'))

