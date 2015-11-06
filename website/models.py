from django.db import models
from django_markdown.models import MarkdownField
import reversion


class Page(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='e.g. "Internet of Things"'
    )
    url = models.SlugField(
        max_length=200,
        help_text='e.g. "things"')

    def __unicode__(self):
        return self.title


class Element(models.Model):
    page = models.ForeignKey(Page, related_name="elements")
    name = models.CharField(
        max_length=200,
        help_text='Friendly name.')
    text = MarkdownField()

    def __unicode__(self):
        return self.name

reversion.register(Element)
reversion.register(Page, follow=['elements'])
