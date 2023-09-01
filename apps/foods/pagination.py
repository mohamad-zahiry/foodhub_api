from rest_framework.pagination import PageNumberPagination


class FoodByCategoryPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 10
    page_size_query_param = "page_size"
