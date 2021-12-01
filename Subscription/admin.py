from django.contrib import admin
from .models import *


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']
    # readonly_fields = ['created_at', 'updated_at']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'price', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

