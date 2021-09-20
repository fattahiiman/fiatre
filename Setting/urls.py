from django.urls import path
from .views import *

urlpatterns = [
    path('', SettingsList.as_view() , name='settings'),
    path('create/', SettingsCreate.as_view() , name='settings-create'),
    path('update/<pk>/', SettingsUpdate.as_view() , name='settings-update'),
    path('delete/<pk>/', SettingsDelete.as_view() , name='settings-delete'),
]
