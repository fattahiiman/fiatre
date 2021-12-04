from django.urls import path
from .views import *

urlpatterns = [
    path('', CouponsList.as_view() , name='coupons'),
    path('create/', CouponsCreate.as_view() , name='coupons-create'),
    path('update/<pk>/', CouponsUpdate.as_view() , name='coupons-update'),
    path('delete/<pk>/', CouponsDelete.as_view() , name='coupons-delete'),

    path('users', CouponUserList.as_view(), name='coupons_user'),
]