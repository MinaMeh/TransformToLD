from django import template
register= template.Library()

@register.filter(name='get_dict')
def get_dict(value):
    return value.items()
    
@register.filter(name='get_value')
def get_value(value,arg):
    return value[arg]