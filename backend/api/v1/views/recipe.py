import sys
from recipes.models import Recipe
from users.models import Subscription
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from django.db.models import Exists, OuterRef

from ..serializers import RecipeCreateUpdate, RecipeListSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecipeListSerializer
    queryset = Recipe.objects.all().prefetch_related('author__subscribing')


class RecipeViewSet(
    viewsets.ModelViewSet
):
    queryset = Recipe.objects.all().prefetch_related('author__subscribing')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
    
        return RecipeCreateUpdate
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Uses this to preserve the original structure of the `ViewSet` class
        # and get `obj` that is saved to DB. 
        obj = self.perform_create(serializer)

        # Changing serializer that is used for `Response` formation
        serializer = RecipeListSerializer(obj, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def perform_create(self, serializer):
        return serializer.save()
