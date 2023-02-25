from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..exceptions import SubscribeActionError
from ..serializers import UserWithRecipes

# Costants with errors messages:
REPITE_SUBSCRIBE_MESSAGE = _(
    'You are trying repeatedly subscribe (unsubscribe)'
)
SELF_SUBSCRIBE_MESSAGE = _(
    'You can not subscribe to yourself'
)


User = get_user_model()


class SubscriptionViewSet(viewsets.GenericViewSet):
    serializer_class = UserWithRecipes

    def get_queryset(self):
        return (
            User.objects.all().
            prefetch_related('recipe_set', 'subscribing')
            .annotate(recipes_count=Count('recipe'))
        )
    
    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        instance = self.get_object()
        if instance == self.request.user:
            raise SubscribeActionError(SELF_SUBSCRIBE_MESSAGE)

        is_subscriber = instance.subscribing.filter(
                user=request.user).exists()
    
        if request.method == 'POST':
            if not is_subscriber:
                instance.subscribing.create(
                    subscribing=instance,
                    user=self.request.user
                )
            else:
                raise SubscribeActionError(REPITE_SUBSCRIBE_MESSAGE)
            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        elif request.method == 'DELETE':
            if is_subscriber:
                instance.subscribing.get(
                    subscribing=instance,
                    user=self.request.user
                ).delete()
            else:
                raise SubscribeActionError(REPITE_SUBSCRIBE_MESSAGE)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            assert False
