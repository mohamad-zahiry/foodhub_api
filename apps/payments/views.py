from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from orders.models import Order

from .utils import get_payment_link


class StartPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_uuid, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, uuid=order_uuid)
        except Order.DoesNotExist:
            msg = "order with uuid: '%s' does not exist" % order_uuid
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        return Response(get_payment_link(request.user, order))
