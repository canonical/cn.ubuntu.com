#!/usr/bin/env python

# Modules
from django.core import serializers
from django.core.management.base import BaseCommand

# Local
from website.models import Page, Element


class Command(BaseCommand):
    help = 'Outputs the data for a page (specified by url) as JSON'

    def add_arguments(self, parser):
        parser.add_argument('url')

    def handle(self, *args, **options):
        url = options['url']

        export_page = Page.objects.get(url=url)
        elements = Element.objects.filter(page=export_page)
        items = [export_page] + list(elements)

        print serializers.serialize(
            'json', items,
            indent=2,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True
        )
