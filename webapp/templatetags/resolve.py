from django import template

register = template.Library()


@register.simple_tag()
def resolve(lookup, target):
    try:
        return target[lookup]

    except (IndexError, KeyError):
        return None
