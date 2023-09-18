from django.urls import path

from .views import (
    CartView,
    CartUpdateView,
    OrderItemDeleteView,
    FinishOrderView,
    OrderStateView,
    OrderListView,
    update_order_state,
)


app_name = "orders"

urlpatterns = [
    path("update/", CartUpdateView.as_view(), name="cart_update"),
    path("delete/<int:pk>/", OrderItemDeleteView.as_view(), name="order_item_delete"),
    path("cart/", CartView.as_view(), name="cart_view"),
    path("finish/", FinishOrderView.as_view(), name="finish_order"),
    path("state/<str:uuid>/", OrderStateView.as_view(), name="order_status"),
    path("", OrderListView.as_view(), name="orders_list"),
    path("chef/update/<str:order_uuid>/", update_order_state, name="chef_update_order_state"),
]
