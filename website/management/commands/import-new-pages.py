#!/usr/bin/env python

# System
import json

# Modules
from django.core.management.base import BaseCommand

# Local
from website.models import Page, Element


class Command(BaseCommand):
    """
    import-new-pages:

    A new manage.py command for importing page data into a database
    from a directory of JSON files.
    """

    help = 'Import all JSON page data from a list of files'

    def add_arguments(self, parser):
        """
        One argument: A list of files containing JSON data
        """

        parser.add_argument('files', nargs='+')

    def handle(self, *args, **options):
        """
        Process the command
        """

        for filepath in options['files']:
            with open(filepath) as page_file:
                data = json.load(page_file)

                page = next(
                    (item for item in data if item['model'] == 'website.page'),
                    None
                )

                # Create the page
                ##

                print "Creating page {}: {}".format(
                    page['fields']['url'],
                    page['fields']['title']
                )
                (page, created) = Page.objects.get_or_create(**page['fields'])

                # Stop if page already existed
                if not created:
                    print "Page already exists. Moving on."
                    continue

                # Create the elements for the page
                ##

                elements = [
                    item for item in data if item['model'] == 'website.element'
                ]

                for item in elements:
                    fields = item['fields']
                    fields['page'] = page

                    # Replace unicode double encodings, like `\\r`
                    # Created by django.serializers
                    for key, value in fields.items():
                        if type(value) is unicode:
                            fields[key] = value.decode('unicode_escape')

                    print "Creating element: " + fields['name']

                    Element.objects.get_or_create(**fields)
