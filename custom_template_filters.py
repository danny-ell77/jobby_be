from django import template

register = template.Library()


@register.filter
def range_from_int(value):
    return range(int(value))
