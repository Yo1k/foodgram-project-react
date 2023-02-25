from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.v1.serializers import CustomUserSerializer
from recipes.models import Recipe

User = get_user_model()


class RecipeMinified(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'name',
            # 'image', # SKTODO not impl'image'
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
            'name',
            # 'image', # SKTODO not impl
            'cooking_time',
        )

class UserWithRecipes(CustomUserSerializer):
    recipes = RecipeMinified(
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
