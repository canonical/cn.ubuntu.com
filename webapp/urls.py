from django.conf.urls import url
from canonicalwebteam.django_views import TemplateFinder
from canonicalwebteam.yaml_responses.django_helpers import (
    create_redirect_views,
)

urlpatterns = create_redirect_views()
urlpatterns += [
    url(r"^(?P<template>.*)[^\/]$", TemplateFinder.as_view()),
    url(r"^$", TemplateFinder.as_view()),
]
