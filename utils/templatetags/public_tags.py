import jdatetime
from django import template

register = template.Library()

@register.filter("jdate", is_safe=False)
def jdatetime_beautify_filter(value, arg=None):
    try:
        if arg:
            try:
                return value.strftime(arg)
            except:
                pass
        return value.strftime("%H:%M, %Y/%m/%d")
    except:
        try:
            return jdatetime.datetime.strptime(str(value), '%Y/%m/%d %H:%M:%S')
        except (ValueError, TypeError):
            return ''