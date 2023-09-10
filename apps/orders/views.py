from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OrderItem, Order
from .serializers import (
    OrderItemSerializer,
    CartSerializer,
    OrderStatusSerializer,
    OrderSerializer,
)
from .utils import get_cart, delete_order_item, finish_order


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
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_cart(self.request.user)

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        try:
            finish_order(order)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(Q(user=self.request.user) & ~Q(status=Order.Status.IN_CART))


class OrderStatusView(generics.RetrieveAPIView):
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(Q(user=self.request.user) & ~Q(status=Order.Status.IN_CART))
