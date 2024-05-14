from django import template

register = template.Library()

@register.filter
def format_phone(value):
    if value is None:
        return ""
    if len(value) == 10:
        return f"({value[0:2]}) {value[2:6]}-{value[6:]}"
    elif len(value) == 11:
        return f"({value[0:2]}) {value[2:7]}-{value[7:]}"
    else:
        return value