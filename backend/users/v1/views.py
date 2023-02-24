from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        return User.objects.all().prefetch_related('subscribing')
