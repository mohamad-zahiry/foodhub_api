from django.urls import path

from .views import (
    CreateUserView,
    ChangePasswordView,
    UpdateUserView,
    UserView,
    AddressView,
    CreateAddressView,
    UpdateDeleteAddressView,
)


basename = "accounts"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("user/", UserView.as_view(), name="user"),
    path("address/", AddressView.as_view(), name="address"),
    path("address/add/", CreateAddressView.as_view(), name="create_address"),
    path(
        "address/update/",
        UpdateDeleteAddressView.as_view(http_method_names=["put"]),
        name="update_address",
    ),
    path(
        "address/delete/",
        UpdateDeleteAddressView.as_view(http_method_names=["delete"]),
        name="delete_address",
    ),
]
