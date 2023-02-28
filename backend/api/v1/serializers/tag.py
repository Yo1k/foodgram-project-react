from recipes.models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag
        read_only_fields = (
            'id',
        )
