#!/usr/bin/env python

# System
import os
import re
import glob

# Modules
from django.core.management.base import BaseCommand
from jinja2 import Template


def latest_migration(migration_dir):
    """
    Get the most recent migration name
    """

    file_search = os.path.join(migration_dir, '[0-9][0-9][0-9][0-9]_*.py')
    files = sorted(glob.glob(file_search))
    last_file = os.path.basename(files[-1])
    return last_file.replace('.py', '')


def next_migration_number(migration_name):
    """
    Get the next migration number as a 4 digit string
    """

    next_number = int(migration_name[0:4]) + 1

    return '%04d' % next_number


class Command(BaseCommand):
    help = """
        Creates a migration to import a specific JSON file for a new page
        into the database
    """

    def add_arguments(self, parser):
        parser.add_argument('page_url')
        parser.add_argument('json_filepath')

    def handle(self, *args, **options):
        page_url = options['page_url']
        json_filepath = options['json_filepath']

        app_name = 'website'
        template_filename = 'replace-page.py.jinja2'

        migration_dir = os.path.join(app_name, 'migrations')

        json_filename = os.path.basename(json_filepath)
        migration_suffix = (
            '_' + re.sub('\.[^.]+$', '', json_filename) + '_replace_page.py'
        )

        existing_migration = glob.glob(
            os.path.join(migration_dir, '*' + migration_suffix)
        )

        previous_migration = latest_migration(migration_dir)
        migration_prefix = next_migration_number(previous_migration)
        output_filename = migration_prefix + migration_suffix

        output_filepath = os.path.join(migration_dir, output_filename)
        template_filepath = os.path.join(
            app_name, 'migrations', template_filename
        )

        # Parse template
        with open(template_filepath) as template:
            parser = Template(template.read())
            migration_contents = parser.render(
                filepath=json_filepath,
                page_url=page_url,
                previous_migration=previous_migration
            )

        print "- Writing migration to " + output_filepath
        # Write output
        with open(output_filepath, 'w') as migration:
            migration.write(migration_contents)
