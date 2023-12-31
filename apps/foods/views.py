from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.utils import permission
from constants import perm_name, P

from .models import Food, Ingredient
from .pagination import FoodByCategoryPagination
from .serializers import FoodCreateSerializer, FoodUpdateSerializer, FoodSerializer, IngredientSerializer


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated, permission(perm_name(P.ADD_DELETE_CHANGE_FOOD))]


class IngredientUpdateView(generics.UpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated, permission(perm_name(P.ADD_DELETE_CHANGE_FOOD))]


class CategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Food.Category.choices)


class FoodByCategoryView(generics.ListAPIView):
    serializer_class = FoodSerializer
    pagination_class = FoodByCategoryPagination

    def get_queryset(self):
        category = self.kwargs["category"].title()
        try:
            Food.Category.labels.index(category)
        except ValueError:
            # if the category doesnt' exist, return empty queryset
            return Food.objects.none()

        return Food.objects.filter(category=category[0])


class ListCreateFoodsView(generics.ListCreateAPIView):
    serializer_class = FoodCreateSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated, permission(perm_name(P.ADD_DELETE_CHANGE_FOOD))]


class FoodUpdateView(generics.UpdateAPIView):
    serializer_class = FoodUpdateSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticated, permission(perm_name(P.ADD_DELETE_CHANGE_FOOD))]


class FoodRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
