from django.urls import path
from .views import *

urlpatterns = [
    path('buy/', pay, name='buy_subscription-payment'),
    path('buy/verify/', verify, name='buy_subscription-verify'),
]
