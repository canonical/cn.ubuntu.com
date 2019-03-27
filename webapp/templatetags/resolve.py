from django import template

register = template.Library()


@register.simple_tag()
def resolve(lookup, target):
    return target[lookup]
