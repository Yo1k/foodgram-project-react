from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.v1.serializers import CustomUserSerializer

from .recipe import RecipeMinifiedSerializer

User = get_user_model()


class UserWithRecipes(CustomUserSerializer):
    recipes = RecipeMinifiedSerializer(
        source='recipe_set',
        many=True
    )
    recipes_count = serializers.IntegerField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = User
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
