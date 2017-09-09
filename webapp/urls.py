from django.conf.urls import url

from .views import CmsTemplateFinder

urlpatterns = [
    url(r'^(?P<template>.*/)?$', CmsTemplateFinder.as_view())
]
