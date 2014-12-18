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
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)
ROOT_URLCONF = 'webapp.urls'
WSGI_APPLICATION = 'webapp.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

TEMPLATE_DIRS = ["templates"]

STATICFILES_FINDERS = ['django_static_root_finder.finders.StaticRootFinder']
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

CACHE_MIDDLEWARE_SECONDS = 3600 / 2
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
