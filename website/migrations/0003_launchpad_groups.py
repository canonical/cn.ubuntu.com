# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Modules
from django.db import migrations
from django.contrib.auth.models import Group
from django.conf import settings


def create_launchpad_groups(apps, schema_editor):
    """
    Create groups needed for SSO
    """

    for group_name in settings.OPENID_LAUNCHPAD_TEAMS_REQUIRED:
        Group.objects.create(name=group_name)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_desktop_page'),
    ]

    operations = [
        migrations.RunPython(create_launchpad_groups)
    ]

