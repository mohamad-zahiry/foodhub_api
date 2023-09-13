from django.urls import path

from .views import StartPaymentView

urlpatterns = [
    path("pay/<str:order_uuid>/", StartPaymentView.as_view(), name="start_payment"),
]
