from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Food
from .pagination import FoodByCategoryPagination
from .serializers import FoodSerializer


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
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
