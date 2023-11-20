from django import template
from django.db.models.query import QuerySet
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

@register.filter
def filter_queryset(obj, user_id):
    if isinstance(obj,QuerySet):
        if obj.filter(rating_by=user_id).exists():
            return obj.filter(rating_by=user_id).first().star_rating
        else:
            return False
    
@register.filter
def subtract(value,arg):
    return value-int(arg)

@register.filter
def filter_proposal(obj,user_id):
    if isinstance(obj,QuerySet):
        queryset= obj.filter(user=user_id)
        if queryset.exists():
            return True
        else:
            return False
    else:
        obj

    
 
    