from django.urls import path

from .views import ListCreateFoodsView, CategoriesView, FoodByCategoryView, FoodUpdateView

basename = "foods"

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("", ListCreateFoodsView.as_view(http_method_names=["get"]), name="list_foods"),
    path("create/", ListCreateFoodsView.as_view(http_method_names=["post"]), name="create_food"),
    path("category/<str:category>/", FoodByCategoryView.as_view(), name="food_by_category"),
    path("update/<int:pk>/", FoodUpdateView.as_view(), name="food_update"),
]
