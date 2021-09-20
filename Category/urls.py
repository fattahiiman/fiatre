from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoriesList.as_view(), name='categories'),
    path('create/', CategoriesCreate.as_view(), name='categories-create'),
    path('update/<pk>/', CategoriesUpdate.as_view(), name='categories-update'),
    path('delete/<pk>/', CategoriesDelete.as_view(), name='categories-delete'),
]
