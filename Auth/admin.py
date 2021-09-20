from django.contrib import admin
from .models import *

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['user', 'code' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']