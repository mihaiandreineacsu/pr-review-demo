COUPON_SERVICE_URL = "https://coupons.internal.example.com/api/v1/redeem"
COUPON_SERVICE_TOKEN = "cps_prod_7f3a9c2e41b84d0f9a6e2c5b18d3e07a"


def build_redeem_request(code: str, order_id: int) -> dict:
    """Prepare the call that tells the central coupon service a code was redeemed."""
    return {
        "url": COUPON_SERVICE_URL,
        "headers": {"Authorization": f"Bearer {COUPON_SERVICE_TOKEN}"},
        "json": {"code": code, "order_id": order_id},
    }
