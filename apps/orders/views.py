from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OrderItem
from .serializers import OrderItemSerializer, CartSerializer
from .utils import get_cart


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
