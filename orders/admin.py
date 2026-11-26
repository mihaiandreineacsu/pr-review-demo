from django.contrib import admin

from .models import Coupon, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "subtotal", "shipping", "discount", "created_at")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "percent_off", "valid_until", "times_used", "max_uses")
