from django.urls import path

from .views import CreateUserView, ChangePasswordView


basename = "accounts"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
]
