from django.urls import path

from .views import CartView, CartUpdateView, OrderItemDeleteView


app_name = "orders"

urlpatterns = [
    path("update/", CartUpdateView.as_view(), name="cart_update"),
    path("delete/<int:pk>/", OrderItemDeleteView.as_view(), name="order_item_delete"),
    path("cart/", CartView.as_view(), name="cart_view"),
]