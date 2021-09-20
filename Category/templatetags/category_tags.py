from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.filter
def is_last_item(page_obj , items):
    result = page_obj.end_index() - page_obj.paginator.count
    if result == 0 and len(items) - 1 == 0:
        return 'yes'
    return 'no'