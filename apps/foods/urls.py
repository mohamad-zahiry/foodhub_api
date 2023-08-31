from django.urls import path

from .views import CategoriesView

basename = "foods"

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
]
