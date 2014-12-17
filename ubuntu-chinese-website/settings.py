"""
Django settings for ubuntu Chinese website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'o@kjnphb9#+3fl80i#$v$+0la3u^atow)b33h*bafbcwir0w04'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['django_versioned_static_url']
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = 'ubuntu-chinese-website.urls'
WSGI_APPLICATION = 'ubuntu-chinese-website.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

TEMPLATE_DIRS = ["templates"]

STATICFILES_FINDERS = ['django_static_root_finder.finders.StaticRootFinder']
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'error_file': {
            'level': 'WARNING',
            'filename': os.path.join(BASE_DIR, 'django-error.log'),
            'class':'logging.handlers.RotatingFileHandler',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 2
        }
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}
