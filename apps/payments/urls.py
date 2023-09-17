from django.urls import path

from .views import StartPaymentView, payment_callback_view

urlpatterns = [
    path("pay/<str:order_uuid>/", StartPaymentView.as_view(), name="start_payment"),
    path("callback/", payment_callback_view, name="payment_callback"),
]
