from django import template
register = template.Library()

@register.filter(name='truncate_chars')
def truncate_chars(value):
    if value.__len__() > 10:
        return '%s......'% value[0:10]
    else:
        return value

@register.filter(name='data_time')
def data_time(value):
    if value:
        return value.strftime('%Y-%m-%d %H:%M');
    else:
        return value

