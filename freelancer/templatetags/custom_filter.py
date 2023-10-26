from django import template

register = template.Library()
@register.filter
def update_variable(value):
    breakpoint()
    data = value
    return data