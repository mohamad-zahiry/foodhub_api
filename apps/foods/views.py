from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Food


class CategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Food.Category.choices)
