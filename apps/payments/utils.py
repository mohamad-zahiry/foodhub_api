from decimal import Decimal

from django.conf import settings

from accounts.models import User
from orders.models import Order
from orders.utils import update_order_price

from .models import Transaction
from .idpay import IDPayAPI, STATUS_SUCCESS


def idpay() -> IDPayAPI:
    return IDPayAPI(
        api_key=settings.IDPAY_API_KEY,
        callback=settings.IDPAY_CALLBACK_URL,
        sandbox=settings.IDPAY_SANDBOX_MODE,
    )


def _normalize_price(price: Decimal):
    """convert the Order.final_price to a value that payment gateway
    can accept that. in this project, IDPay accepts Rials as unit."""
    return int(float(price) * 100)


def get_payment_link(user: User, order: Order) -> str:
    tcn, create = Transaction.objects.get_or_create(user=user, order_uuid=order.uuid)
    update_order_price(order)

    if not create:
        return tcn.payment_link

    operation = idpay().payment(
        order.id,
        _normalize_price(order.final_price),
        {
            "name": user.name,
            "phone": str(user.phone),
            "mail": user.email,
            "desc": "foodhub order payment",
        },
    )

    if operation["status"] == STATUS_SUCCESS:
        tcn.payment_id = operation["response"]["id"]
        tcn.payment_link = operation["response"]["link"]
        tcn.save()

    return tcn.payment_link
