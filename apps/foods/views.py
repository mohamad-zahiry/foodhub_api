from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Food
from .serializers import FoodSerializer


class CategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Food.Category.choices)


class ListCreateFoodsView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
