from django import template

register = template.Library()

@register.filter
def remove_extra(value):
    return value.replace("_extra","")