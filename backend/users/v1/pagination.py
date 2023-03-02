from rest_framework.pagination import PageNumberPagination


class CustomUserResultPagination(PageNumberPagination):
    page_size_query_param = 'limit'
