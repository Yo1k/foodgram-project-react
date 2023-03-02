from django.db.models import Exists, OuterRef
from django_filters import rest_framework as df_filters
from recipes.models import Favorite, Recipe, ShoppingCart
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..filters import RecipeFilter
from ..pagination import RecipeResultPagination
from ..permissions import IsAuthorOrAdminOrReadOnly
from ..serializers import RecipeCreateUpdateSerializer, RecipeListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = (df_filters.DjangoFilterBackend,)
    filterset_class  = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = RecipeResultPagination
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        favorite_expr = Favorite.objects.filter(
            recipe=OuterRef('pk'),
            user__id=self.request.user.id
        )
        shopping_cart_expr = ShoppingCart.objects.filter(
            recipe=OuterRef('pk'),
            user__id=self.request.user.id
        )

        queryset = (
            Recipe.objects.all()
            .prefetch_related('author__subscribing')
            .annotate(is_favorited=Exists(favorite_expr))
            .annotate(is_in_shopping_cart=Exists(shopping_cart_expr))
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
    
        return RecipeCreateUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Uses this to preserve the original structure
        # of the `ModelViewSet` class and get `obj` that is saved to DB. 
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

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Uses this to preserve the original structure
        # of the `ModelViewSet` class and get `obj` that is saved to DB. 
        obj = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Changing serializer that is used for `Response` formation
        serializer = RecipeListSerializer(obj, context={'request': request})
        return Response(serializer.data)
