# Modules
from django.db import models
from django_markdown.models import MarkdownField
from django.contrib.auth.models import User, Group
from django_openid_auth.signals import openid_login_complete
from django.db.models.signals import pre_save
from django.conf import settings
from reversion import revisions as reversion


class PageManager(models.Manager):
    """
    The manager class for retrieving Pages
    Extended to support getting elements with a natural key
    - The url (which will always be unique)
    """

    def get_by_natural_key(self, url):
        return self.get(url=url)


class Page(models.Model):
    """
    A page model contains the dynamic data for a page of the website
    It can be edited in the CMS.
    A page has many Elements.
    """

    managed = True
    objects = PageManager()

    title = models.CharField(
        max_length=200,
        help_text='e.g. "Internet of Things"'
    )
    url = models.SlugField(
        max_length=200,
        help_text='e.g. "things"',
        unique=True
    )

    def __unicode__(self):
        return self.title

    def natural_key(self):
        return (self.url,)


class ElementManager(models.Manager):
    """
    The manager class for retrieving Elements
    Extended to support getting elements with a natural key
    - The combination of the page and the element name
    """

    def get_by_natural_key(self, page, name):
        return self.get(page=page, name=name)


class Element(models.Model):
    """
    Elements belong to Pages. They are text blocks which can be
    inserted into templates, and can be edited in the CMS admin.
    """

    managed = True
    objects = ElementManager()

    page = models.ForeignKey(Page, related_name="elements")
    name = models.CharField(
        max_length=200,
        help_text='Friendly name.')
    text = MarkdownField()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.page, self.name)

    class Meta:
        unique_together = (('page', 'name'),)


def make_user_admin(sender, **kwargs):
    """
    Update all created users to become admin users (is_staff)
    and make them superusers if they're in the SUPERUSER_GROUP
    """

    # Get user from openid object
    user_id = sender.objects.first().user_id
    user = User.objects.get(id=user_id)

    # All users are staff (can use admin)
    user.is_staff = True

    # Superuser if in superuser group
    group_names = [group.name for group in user.groups.all()]
    user.is_superuser = settings.SUPERUSER_GROUP in group_names

    user.save()


reversion.register(Element)
reversion.register(Page, follow=['elements'])

openid_login_complete.connect(make_user_admin)

