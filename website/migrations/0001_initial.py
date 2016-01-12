# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Friendly name.', max_length=200)),
                ('text', django_markdown.models.MarkdownField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'e.g. "Internet of Things"', max_length=200)),
                ('url', models.SlugField(help_text=b'e.g. "things"', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='element',
            name='page',
            field=models.ForeignKey(related_name='elements', to='website.Page'),
        ),
    ]
