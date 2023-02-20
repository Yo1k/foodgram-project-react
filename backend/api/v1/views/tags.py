from recipes.models import Tag
from rest_framework import viewsets

from ..serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
