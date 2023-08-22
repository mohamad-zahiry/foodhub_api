from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CreateUserSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
)
from .models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
