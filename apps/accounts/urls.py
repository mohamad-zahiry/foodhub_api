from django.urls import path

from .views import CreateUserView


basename = "accounts"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
]
