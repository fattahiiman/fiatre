from django.urls import path
from .views import *

urlpatterns = [
    path('create/', Subscriptions_Create.as_view(), name='subscriptions-create'),
    path('update/<pk>/', Subscriptions_Update.as_view(), name='subscriptions-update'),
    path('delete/<pk>/', Subscriptions_Delete.as_view(), name='subscriptions-delete'),

    path('types/', Subscriptions_Types_List.as_view(), name='types'),
    path('types/create/', Subscriptions_Types_Create.as_view(), name='types-create'),
    path('types/update/<pk>/', Subscriptions_Types_Update.as_view(), name='types-update'),
    path('types/delete/<pk>/', Subscriptions_Types_Delete.as_view(), name='types-delete'),
]
