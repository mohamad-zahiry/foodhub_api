from uuid import UUID

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from orders.models import Order

from .utils import (
    get_payment_link,
    get_transaction,
    verify_transaction,
    order_state_cooking,
)


class StartPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_uuid, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, uuid=order_uuid)
        except Order.DoesNotExist:
            msg = "order with uuid: '%s' does not exist" % order_uuid
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        return Response(get_payment_link(request.user, order))


@api_view(["post"])
def payment_callback_view(request):
    order_uuid = None
    if not settings.IDPAY_SANDBOX_MODE:
        order_uuid = UUID(int=request.data.get("order_id"))

    id = request.data.get("id")
    status = int(request.data.get("status"))

    if status == 10:
        tcn = get_transaction(id, order_uuid)
        if verify_transaction(tcn):
            order_state_cooking(tcn)
            return Response("verified")

    return Response("not verified")
