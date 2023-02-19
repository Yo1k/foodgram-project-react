from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from djoser.views import UserViewSet

from .models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        subscription_expr = Subscription.objects.filter(
            subscribing=OuterRef('pk'),
            user=self.request.user
        )
        return User.objects.annotate(
            is_subscribed=Exists(subscription_expr)
        )
