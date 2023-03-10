from rest_framework import (
    filters,
    viewsets
)
from rest_framework.permissions import AllowAny

from recipes.models import Ingredient

from ..serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter]
    pagination_class = None
    permission_classes = [AllowAny]
    search_fields = ['^name', ]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
