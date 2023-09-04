from django.urls import path

from .views import CartUpdateView


app_name = "orders"

urlpatterns = [
    path("update/", CartUpdateView.as_view(), name="cart_update"),
]
