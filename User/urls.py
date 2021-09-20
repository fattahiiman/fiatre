from django.urls import path
from .views import *

urlpatterns = [
    path('', UsersList.as_view(), name='users'),
    path('create/', UsersCreate.as_view(), name='users-create'),
    path('update/<pk>/', UsersUpdate.as_view(), name='users-update'),
    path('delete/<pk>/', UsersDelete.as_view(), name='users-delete'),
]
