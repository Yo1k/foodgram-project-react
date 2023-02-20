from recipes.models import Ingredient
from rest_framework import filters, viewsets

from ..serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    search_fields = ['^name',]
