from django.conf.urls import include, url
from django.contrib import admin

from views import CmsTemplateFinder

urlpatterns = [
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url('^markdown/', include('django_markdown.urls')),
    url(r'^(?P<template>.*/)?$', CmsTemplateFinder.as_view())
]
