from recipes.models import Tag
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


from ..serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
