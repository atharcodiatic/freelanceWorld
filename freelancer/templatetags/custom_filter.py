from django import template

register = template.Library()
@register.filter
def update_variable(value,arg):
    value = arg 
    return value

@register.filter
def multiply(value, arg):
    # you would need to do any localization of the result here
    return int(value) * int(arg)

@register.filter
def divide(value, arg):
    converted = int(float(value)) / int(float(arg))
    return float("{:.2f}".format(converted))
 
    