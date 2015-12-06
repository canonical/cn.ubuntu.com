#!/usr/bin/env python

# System
import os
import re

# Modules
from django.core import serializers
from django.core.management.base import BaseCommand
from jinja2 import Template

# Local
from website.models import Page, Element


def create_page_migration(json_filepath, app_name='website'):
    """
    Make a custom data migration inside 'website/migrations'
    to migrate the new page into the database
    """

    template_filename = 'page.py.jinja2'

    json_filename = os.path.basename(json_filepath)
    output_filename = re.sub('\.[^.]+$', '', json_filename) + '_page.py'

    output_filepath = os.path.join(app_name, 'migrations', output_filename)
    template_filepath = os.path.join(app_name, 'migrations', template_filename)

    # Parse template
    with open(template_filepath) as template:
        parser = Template(template.read())
        migration_contents = parser.render(filepath=json_filepath)

    print "- Writing migration to " + output_filepath
    # Write output
    with open(output_filepath, 'w') as migration:
        migration.write(migration_contents)


class Command(BaseCommand):
    help = 'Outputs the data for a page (specified by url) as JSON'

    def add_arguments(self, parser):
        parser.add_argument('url')

    def handle(self, *args, **options):
        url = options['url']
        page_name = url.replace('/', '-')

        target_filepath = os.path.join(
            'website', 'page-data', page_name + '.json'
        )

        export_page = Page.objects.get(url=url)
        elements = Element.objects.filter(page=export_page)
        items = [export_page] + list(elements)

        page_json = serializers.serialize(
            'json', items,
            indent=2,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True
        )

        print "- Writing data to " + target_filepath
        with open(target_filepath, 'w') as json_file:
            json_file.write(page_json)

        create_page_migration(target_filepath)
