from django.urls import path

from .views import ListCreateFoodsView, CategoriesView, FoodByCategoryView, FoodUpdateDestroyView, FoodView

basename = "foods"

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("", ListCreateFoodsView.as_view(http_method_names=["get"]), name="list_foods"),
    path("create/", ListCreateFoodsView.as_view(http_method_names=["post"]), name="create_food"),
    path("category/<str:category>/", FoodByCategoryView.as_view(), name="food_by_category"),
    # FoodView with get method must be above the other routes, because it is not using authetication
    path("<int:pk>/", FoodView.as_view(http_method_names=["get"]), name="view_food"),
    path("<int:pk>/", FoodUpdateDestroyView.as_view(http_method_names=["put"]), name="update_food"),
    path("<int:pk>/", FoodUpdateDestroyView.as_view(http_method_names=["delete"]), name="delete_food"),
]
