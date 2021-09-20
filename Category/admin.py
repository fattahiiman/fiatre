from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']