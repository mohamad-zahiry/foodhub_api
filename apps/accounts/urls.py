from django.urls import path

from .views import (
    CreateUserView,
    ChangePasswordView,
    UpdateUserView,
    UserView,
    AddressView,
    CreateAddressView,
    UpdateDeleteAddressView,
    AddCustomerView,
    AddChefView,
    AddAdminView,
)


basename = "accounts"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("user/", UserView.as_view(), name="user"),
    path("add/customer/", AddCustomerView.as_view(), name="add_customer"),
    path("add/chef/", AddChefView.as_view(), name="add_chef"),
    path("add/admin/", AddAdminView.as_view(), name="add_admin"),
    path("address/", AddressView.as_view(), name="address"),
    path("address/add/", CreateAddressView.as_view(), name="create_address"),
    path("address/update/", UpdateDeleteAddressView.as_view(http_method_names=["put"]), name="update_address"),
    path("address/delete/", UpdateDeleteAddressView.as_view(http_method_names=["delete"]), name="delete_address"),
]
