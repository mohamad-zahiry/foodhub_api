from decimal import Decimal
from uuid import UUID

from django.conf import settings
from rest_framework.exceptions import ValidationError

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
    return int(float(price) * 100 * 1000)


def get_payment_link(user: User, order: Order) -> str:
    tcn, create = Transaction.objects.get_or_create(user=user, order_uuid=order.uuid)
    update_order_price(order)

    if tcn.payment_link:
        return tcn.payment_link

    operation = idpay().payment(
        tcn.order_uuid.int,
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


def get_transaction(payment_id: str, order_uuid: UUID = None) -> Transaction:
    if settings.IDPAY_SANDBOX_MODE:
        try:
            return Transaction.objects.get(payment_id=payment_id)
        except Transaction.DoesNotExist:
            msg = "no payment with payment-id=%s found" % (id)
            raise ValidationError(msg)

    try:
        return Transaction.objects.get(order_uuid=order_uuid, payment_id=payment_id)
    except Transaction.DoesNotExist:
        msg = "no payment with order-uuid=%s and payment-id=%s found" % (order_uuid, id)
        raise ValidationError(msg)


def transaction_state(status: int):
    if status == 10:
        return Transaction.State.PAID
    if status >= 100:
        return Transaction.State.VERIFIED
    return Transaction.State.NOT_PAID


def verify_transaction(tcn: Transaction) -> bool:
    if tcn.state == Transaction.State.VERIFIED:
        return False

    if settings.IDPAY_SANDBOX_MODE:
        tcn.state = Transaction.State.VERIFIED
        tcn.save()
        return True

    status, res = idpay().verify(
        id=tcn.payment_id,
        order_id=tcn.order_uuid.int,
    )
    tcn.state = transaction_state(res["status"])
    tcn.save()
    return status == STATUS_SUCCESS


def order_state_cooking(tcn: Transaction):
    if tcn.state == Transaction.State.VERIFIED:
        order = Order.objects.get(uuid=tcn.order_uuid)
        order.state = Order.State.COOK
        order.save()
        return True
    raise ValidationError("order (uuid=%s) has not payed" % tcn.order_uuid)
