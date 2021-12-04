from django.contrib import admin
from .models import *

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'time', 'percent' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CouponUser)
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']