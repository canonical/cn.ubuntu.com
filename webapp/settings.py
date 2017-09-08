"""
Django settings for china project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'no_secret')

WHITENOISE_MAX_AGE = 31557600
WHITENOISE_ALLOW_ALL_ORIGINS = False

DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = ["*"]
APPEND_SLASH = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django_openid_auth',
    'whitenoise.runserver_nostatic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_markdown',
    'markdown_deux',
    'reversion',
    'reversion_compare',
    'canonicalwebteam',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

STATICFILES_FINDERS = [
    'django_static_root_finder.finders.StaticRootFinder',
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
]
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
        },
    },
]
MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    },
}
WSGI_APPLICATION = 'webapp.wsgi.application'

# Django openID auth
# ===

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'

SUPERUSER_GROUP = 'canonical-webmonkeys'
GROUP_PERMISSIONS = [
    'change_element',
    'change_page',
    'add_revision',
    'change_revision',
    'delete_revision',
    'add_version',
    'change_version',
    'delete_version'
]

OPENID_CREATE_USERS = True
OPENID_SSO_SERVER_URL = 'https://login.launchpad.net/'
OPENID_LAUNCHPAD_TEAMS_REQUIRED = [
    'canonical-content-people',
    'canonical-webmonkeys'
]
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True

