# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Modules
from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions
from django.conf import settings


def create_launchpad_groups(apps, schema_editor):
    """
    Create groups needed for SSO
    """

    # Make sure permissions exist
    apps.models_module = True
    create_permissions(apps)

    for group_name in settings.OPENID_LAUNCHPAD_TEAMS_REQUIRED:
        new_group = Group.objects.create(name=group_name)

        for permission_codename in settings.GROUP_PERMISSIONS:
            permissions = Permission.objects.filter(
                codename=permission_codename
            )

            for permission in permissions:
                new_group.permissions.add(permission)

        new_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_server_page'),
    ]

    operations = [
        migrations.RunPython(create_launchpad_groups)
    ]

