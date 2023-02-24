import sys

from django.core.exceptions import ValidationError
from django.http import Http404
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.v1.serializers import CustomUserSerializer
from .tags import TagSerializer

class IngredientInRecipeCreateSerializer(
    serializers.HyperlinkedModelSerializer
    ):
    id = serializers.IntegerField(min_value=1)

    class Meta:
        fields = (
            'id',
            'amount',
        )
        model = IngredientAmount
        read_only_fields = (
        'id',
    )


class IngredientInRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        model = IngredientAmount
        read_only_fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeCreateUpdate(serializers.ModelSerializer):
    ingredients = IngredientInRecipeCreateSerializer(
        source='ingredientamount_set',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
        )

    class Meta:
        fields = (
            'id',
            'ingredients',
            'tags',
            # 'image', SKTODO
            'name',
            'text',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
        )
    # SKTODO переделать на exists()
    def __save_related_ingredients(self, ingredients_data, obj):
        if not ingredients_data:
            return None
        
        
        # ingredient_ids = Ingredient.objects.all().values_list('id', flat=True)
        # for ingredient in ingredients_data:
        #     if ingredient['id'] not in ingredient_ids:
        #         raise serializers.ValidationError(
        #             f'There is no ingrediet with id={ingredient["id"]}'
        #         )
        try:
            for ingrediet in ingredients_data:
                ingredient_id = ingrediet['id']
                get_object_or_404(
                    Ingredient,
                    id=ingredient_id
                )
        except Http404:
            raise serializers.ValidationError(
                f'There is no ingrediet with id={ingredient_id}'
            )
        
        for ingredient_data in ingredients_data:
            obj.ingredients.add(
                ingredient_data['id'],
                through_defaults={'amount': ingredient_data['amount']}
            )

    def __save_related_tags(self, tags_data, obj):
        if tags_data:
            try:
                for tag in tags_data:
                    get_object_or_404(
                        Tag,
                        id=tag.id
                    )
            except Http404:
                raise serializers.ValidationError(
                    f'There is no tag with id={tag.id}'
                )
            obj.tags.set(tags_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredientamount_set', None)
        tags_data = validated_data.pop('tags', None)

        recipe = Recipe(
            author=self.context.get('request').user,
            # ingredients=self.__get_ingredients(ingredients_data), SKTODO
            **validated_data
        )
        try:
            recipe.full_clean()
            # SKTODO проверки, что ингредиенты и тэги сущесвуют, после сохрн.
            recipe.save()
            self.__save_related_ingredients(ingredients_data, recipe)
            self.__save_related_tags(tags_data, recipe)
            return recipe

        except (ValidationError, serializers.ValidationError) as e:
            raise e #serializers.ValidationError(e)
    
    # def update(self, instance, validated_data):
    #     ...


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited', SKTODO
            # 'is_in_shopping_cart', SKTODO
            'name',
            # 'image', SKTODO
            'text',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited', SKTODO
            # 'is_in_shopping_cart', SKTODO
            'name',
            # 'image', SKTODO
            'text',
            'cooking_time',
        )
