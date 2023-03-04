from django.utils.translation import gettext_lazy as _
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe

from ..exceptions import FavoriteActionError
from ..serializers import RecipeMinifiedSerializer

# Constants with errors messages:
REPITE_FAVORITE_ACTION_MESSAGE = _(
    'You are trying repeatedly add (delete) the same recipe to favorite'
)


class FavoriteRecipesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeMinifiedSerializer

    def get_queryset(self):
        return Recipe.objects.all().prefetch_related('favorite_set')

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        instance = self.get_object()

        is_favorited = instance.favorite_set.filter(
            user=request.user
        ).exists()

        if request.method == 'POST':
            if not is_favorited:
                instance.favorite_set.create(
                    recipe=instance,
                    user=self.request.user
                )
            else:
                raise FavoriteActionError(REPITE_FAVORITE_ACTION_MESSAGE)
            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        if request.method == 'DELETE':
            if is_favorited:
                instance.favorite_set.get(
                    recipe=instance,
                    user=self.request.user
                ).delete()
            else:
                raise FavoriteActionError(REPITE_FAVORITE_ACTION_MESSAGE)

            return Response(status=status.HTTP_204_NO_CONTENT)

        assert False
