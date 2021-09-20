from Subscription.templatetags.front_tags import persian_int
from django.contrib.humanize.templatetags.humanize import intcomma

def PersianizeAmount(amount):
    amount = intcomma(amount , False)
    amount = persian_int(amount)
    print('################')
    print(amount)
    return amount