from dateutil.relativedelta import relativedelta
from django import template
from django.contrib.auth import get_user_model
from django.utils import timezone
import jdatetime

register = template.Library()
User = get_user_model()

@register.filter
def check_subscription_expiration(user):
    print('++++++++++++++++')
    print(user.get_subscription())
    print(user.get_subscription().created_at)
    print(relativedelta(months=user.get_subscription().type.time))
    if user.get_subscription():
        today = timezone.now()
        expiration = user.get_subscription().created_at + relativedelta(months=user.get_subscription().type.time)

        print('***********************')
        print(expiration)

        if expiration >= today:
            return True

    return False


@register.filter
def show_expiration(user):
    expiration = user.get_subscription().created_at + relativedelta(months=user.get_subscription().type.time)
    return jdatetime.datetime.fromgregorian(datetime=expiration)


@register.filter
def show_type_expiration(type):
    expiration = type.created_at + relativedelta(months=type.time)
    return jdatetime.datetime.fromgregorian(datetime=expiration)


@register.simple_tag
def check_color(color_counter):
    if color_counter == 2:
        color_counter = 0
    else:
        color_counter += 1
    return color_counter


@register.simple_tag
def show_color(color_counter , colors):
    return colors[color_counter]


@register.filter
def persian_int(string):
    persianize = dict(zip("0123456789",'۰۱۲۳۴۵۶۷۸۹'))
    return ''.join(persianize[digit] if digit in persianize else digit for digit in str(string))