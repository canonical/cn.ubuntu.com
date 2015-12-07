# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Modules
from django.db import migrations

# Local
from website.db_helpers import import_page_from_json_file


def import_page(apps, schema_editor):
    """
    Import a new page from a JSON data in the "page-data" directory
    """

    import_page_from_json_file('website/page-data/cloud.json')


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_phone_page'),
    ]

    operations = [
        migrations.RunPython(import_page)
    ]