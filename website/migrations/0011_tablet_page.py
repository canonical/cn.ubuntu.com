# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Modules
from django.db import migrations

# Local
from website.models import Page
from website.db_helpers import import_page_from_json_file


def import_page(apps, schema_editor):
    """
    Import a new page from a JSON data in the "page-data" directory
    """

    if Page.objects.filter(url="tablet").exists():
        Page.objects.get(url="tablet").delete()

    import_page_from_json_file('website/page-data/tablet.json')


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_launchpad_groups'),
    ]

    operations = [
        migrations.RunPython(import_page)
    ]