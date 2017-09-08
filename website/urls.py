from django.conf.urls import include, url

from .views import CmsTemplateFinder

urlpatterns = [
    url(r'^(?P<template>.*/)?$', CmsTemplateFinder.as_view())
]

