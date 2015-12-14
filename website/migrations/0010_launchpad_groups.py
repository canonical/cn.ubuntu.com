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

    for group_name in settings.OPENID_LAUNCHPAD_TEAMS_REQUIRED:
        Group.objects.create(name=group_name)

    # Create permissions
    for app in apps.get_app_configs():
        create_permissions(app)

    # Special permissions for content editors
    content_people = Group.objects.get(name="canonical-content-people")

    permission_codenames = [
        'change_element',
        'change_page',
        'add_revision',
        'change_revision',
        'delete_revision',
        'add_version',
        'change_version',
        'delete_version'
    ]

    for permission_codename in permission_codenames:
        permissions = Permission.objects.filter(
            codename=permission_codename
        )

        for permission in permissions:
            content_people.permissions.add(permission)


    content_people.save()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_server_page'),
    ]

    operations = [
        migrations.RunPython(create_launchpad_groups)
    ]

