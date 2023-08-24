from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import User, Address
from .serializers import ChangeGroupSerializer


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


class ChangeGroupMixin(generics.CreateAPIView):
    serializer_class = ChangeGroupSerializer
    group = ""
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={
                "sender": self.get_object(),
                "group": Group.objects.get(name=self.group),
            },
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
