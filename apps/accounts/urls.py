from django.urls import path

from .views import CreateUserView, ChangePasswordView, UpdateUserView, UserView


basename = "accounts"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("user/", UserView.as_view(), name="user"),
]
