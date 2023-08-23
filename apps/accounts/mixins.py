from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import User, Address


class UserViewMixin:
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressViewMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Address.objects.filter(user=self.request.user)

    def get_object(self):
        pk = self.request.data["pk"]
        return get_object_or_404(self.get_queryset(), pk=pk)
