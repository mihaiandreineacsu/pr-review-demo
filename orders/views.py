import json
from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Coupon, Order
from .services import build_redeem_request


def serialize_order(order: Order) -> dict:
    return {
        "id": order.id,
        "subtotal": str(order.subtotal),
        "shipping": str(order.shipping),
        "discount": str(order.discount),
        "total": str(order.total),
    }


@login_required
@require_GET
def order_detail(request, order_id: int):
    # Customers may only see their own orders.
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return JsonResponse(serialize_order(order))


@csrf_exempt
@require_POST
def apply_coupon(request, order_id: int):
    data = json.loads(request.body)
    code = data.get("code", "")

    order = Order.objects.get(id=order_id)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, percent_off, valid_until, max_uses, times_used "
            f"FROM orders_coupon WHERE code = '{code}'"
        )
        row = cursor.fetchone()

    if row is None:
        return JsonResponse({"error": "Unknown coupon"}, status=404)

    coupon_id, percent_off, valid_until, max_uses, times_used = row

    if date.fromisoformat(str(valid_until)) < date.today():
        return JsonResponse({"error": "Coupon expired"}, status=400)

    if times_used > max_uses:
        return JsonResponse({"error": "Coupon fully redeemed"}, status=400)

    discount = float(order.subtotal + order.shipping) * percent_off / 100
    order.discount = order.discount + Decimal(discount)
    order.save()

    Coupon.objects.filter(id=coupon_id).update(times_used=F("times_used") + 1)

    redeem_request = build_redeem_request(code, order.id)
    print(f"DEBUG redeem request: {redeem_request}")

    return JsonResponse(serialize_order(order))
