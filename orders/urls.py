from django.urls import path

from . import views

urlpatterns = [
    path("<int:order_id>/", views.order_detail, name="order-detail"),
    path("<int:order_id>/coupon/", views.apply_coupon, name="apply-coupon"),
]
