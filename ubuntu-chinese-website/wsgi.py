"""
WSGI config for canonical project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

# standard
import os
import sys

# third party
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ubuntu-chinese-website.settings"
)

application = get_wsgi_application()
application = Cling(get_wsgi_application())
