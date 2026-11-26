from decimal import Decimal

from django.conf import settings
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=32, unique=True)
    percent_off = models.PositiveIntegerField()
    valid_until = models.DateField()
    max_uses = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.code} (-{self.percent_off}%)"


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("4.90"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.shipping - self.discount

    def __str__(self) -> str:
        return f"Order #{self.pk} ({self.customer})"
