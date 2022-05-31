from django import template

register = template.Library()

@register.filter
def plus_to_slash(value):
    return value.replace("+","/")

