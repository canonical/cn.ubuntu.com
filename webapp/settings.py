"""
Django settings for china project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BLOG_CONFIG = {
    "TAGS_ID": [3265],
    "EXCLUDED_TAGS": [],
    # the title of the blog
    "BLOG_TITLE": "博客",
    # the tag name for generating a feed
    "TAG_NAME": "lang:cn",
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "no_secret")

WHITENOISE_MAX_AGE = 31557600
WHITENOISE_ALLOW_ALL_ORIGINS = False

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = ["whitenoise.runserver_nostatic", "canonicalwebteam"]

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"]

ROOT_URLCONF = "webapp.urls"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

ASSET_SERVER_URL = (
    "https://res.cloudinary.com/"
    "canonical/image/fetch/q_auto,f_auto/"
    "https://assets.ubuntu.com/v1/"
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django_asset_server_url.asset_server_url",
                "django.template.context_processors.request",
            ]
        },
    }
]
MARKDOWN_DEUX_STYLES = {
    "default": {"extras": {"code-friendly": None}, "safe_mode": False}
}
WSGI_APPLICATION = "webapp.wsgi.application"
