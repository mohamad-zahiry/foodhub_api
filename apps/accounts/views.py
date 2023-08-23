from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CreateUserSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
    AddressSerailizer,
    CreateAddressSerailizer,
    UpdateDeleteAddressSerailizer,
)
from .mixins import UserViewMixin, AddressViewMixin


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class ChangePasswordView(UserViewMixin, generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer


class UpdateUserView(UserViewMixin, generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer


class UserView(UserViewMixin, generics.RetrieveAPIView):
    serializer_class = UpdateUserSerializer


class AddressView(AddressViewMixin, generics.ListAPIView):
    serializer_class = AddressSerailizer


class CreateAddressView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateAddressSerailizer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UpdateDeleteAddressView(
    AddressViewMixin, mixins.DestroyModelMixin, generics.UpdateAPIView
):
    serializer_class = UpdateDeleteAddressSerailizer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
