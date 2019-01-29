"""
Django settings for china project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "no_secret")

WHITENOISE_MAX_AGE = 31557600
WHITENOISE_ALLOW_ALL_ORIGINS = False

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = ["whitenoise.runserver_nostatic", "canonicalwebteam"]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = "webapp.urls"

STATIC_ROOT = "static"
STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request"
            ]
        },
    }
]
MARKDOWN_DEUX_STYLES = {
    "default": {"extras": {"code-friendly": None}, "safe_mode": False}
}
WSGI_APPLICATION = "webapp.wsgi.application"
