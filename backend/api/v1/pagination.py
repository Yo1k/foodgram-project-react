from rest_framework.pagination import PageNumberPagination


class RecipeResultPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class SubscriptionResultPagination(PageNumberPagination):
    page_size_query_param = 'limit'
