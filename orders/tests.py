from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order

User = get_user_model()


class OrderDetailTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pw-alice")
        self.bob = User.objects.create_user("bob", password="pw-bob")
        self.order = Order.objects.create(customer=self.alice, subtotal=Decimal("50.00"))

    def test_owner_can_see_order(self):
        self.client.login(username="alice", password="pw-alice")
        response = self.client.get(reverse("order-detail", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], "54.90")

    def test_other_user_gets_404(self):
        self.client.login(username="bob", password="pw-bob")
        response = self.client.get(reverse("order-detail", args=[self.order.id]))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse("order-detail", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)


class ApplyCouponTests(TestCase):
    def setUp(self):
        from datetime import date, timedelta

        from .models import Coupon

        self.alice = User.objects.create_user("alice", password="pw-alice")
        self.order = Order.objects.create(customer=self.alice, subtotal=Decimal("50.00"))
        Coupon.objects.create(
            code="WELCOME10",
            percent_off=10,
            valid_until=date.today() + timedelta(days=30),
        )

    def test_apply_valid_coupon(self):
        self.client.login(username="alice", password="pw-alice")
        response = self.client.post(
            reverse("apply-coupon", args=[self.order.id]),
            data={"code": "WELCOME10"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal("49.41"))
