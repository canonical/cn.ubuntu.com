from django.urls import re_path, path, include
from canonicalwebteam.django_views import TemplateFinder
from canonicalwebteam.yaml_responses.django_helpers import (
    create_redirect_views,
)

urlpatterns = create_redirect_views()
urlpatterns += [
    path(r"blog", include("canonicalwebteam.blog.django.urls")),
    re_path(r"^(?P<template>.*)$", TemplateFinder.as_view()),
    path(r"", TemplateFinder.as_view()),
]
