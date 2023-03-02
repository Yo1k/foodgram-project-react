from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .pagination import CustomUserResultPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomUserResultPagination

    def get_queryset(self):
        return User.objects.all().prefetch_related('subscribing')
