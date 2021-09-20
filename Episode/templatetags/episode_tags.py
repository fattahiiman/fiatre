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




@register.filter(name='addclass')
def add_classes(value, arg):
    '''
    Add provided classes to form field
    :param value: form field
    :param arg: string of classes seperated by ' '
    :return: edited field
    '''
    css_classes = value.field.widget.attrs.get('class', '')
    # check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    # prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    # join back to single string
    return value.as_widget(attrs={'class': ' '.join(css_classes)})
