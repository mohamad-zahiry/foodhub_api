from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, NotFound, ValidationError

from constants import P, perm_name


from .models import OrderItem, Order
from .serializers import (
    OrderItemSerializer,
    CartSerializer,
    OrderStateSerializer,
    OrderSerializer,
    FinishOrderSerializer,
)
from .utils import get_cart, delete_order_item, chef_update_order_state


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_cart(self.request.user)


class CartUpdateView(generics.GenericAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        delete_order_item(instance)


class FinishOrderView(generics.UpdateAPIView):
    serializer_class = FinishOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_cart(self.request.user)


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(Q(user=self.request.user) & ~Q(state=Order.State.ORDER))


class OrderStateView(generics.RetrieveAPIView):
    serializer_class = OrderStateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        return Order.objects.filter(Q(user=self.request.user) & ~Q(state=Order.State.ORDER))


@api_view(["POST"])
def update_order_state(request, order_uuid):
    if not request.user.has_perms([perm_name(P.CHANGE_ORDER_STATUS)]):
        raise NotAuthenticated("you can not do this action")

    states = {
        "cook": Order.State.COOK,
        "delivery": Order.State.DELIVERY,
    }
    try:
        state = states[request.data.get("state")]
        order = Order.objects.get(uuid=order_uuid)

    except KeyError:
        raise ValidationError('use like this: {"state": "cook|delivery"}')

    except Order.DoesNotExist:
        raise NotFound("order (uuid=%s) does not exist" % order_uuid)

    except DjangoValidationError:
        raise ValidationError("%s is not a valid order uuid" % order_uuid)

    chef_update_order_state(order, state)
    serializer = OrderStateSerializer(instance=order)
    return Response(serializer.data, status=status.HTTP_200_OK)
