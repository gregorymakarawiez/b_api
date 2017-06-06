from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def add_class(value, css):
    return value.as_widget(attrs={"class":css})


@register.filter
def index(List, i):
    #return List[int(i)]
    return List[i]

@register.filter
def label(field):
# return label defined in form field
    try:
        label=field.auto_id
    except AttributeError:
        label=""
    return label

@register.filter
def required(field):
# return True if field is required
    try:
        is_required=field.field.required
    except AttributeError:
        is_required=False
    return is_required

@register.filter
def escapenewline(value):
    """
    Adds a slash before any newline. Useful for loading a multi-line html chunk
    into a Javascript variable.
    """
    return value.replace('\n', '\\\n')
escapenewline.is_safe = True
escapenewline = stringfilter(escapenewline)



