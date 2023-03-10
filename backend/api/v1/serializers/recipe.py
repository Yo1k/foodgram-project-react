import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag
)
from users.v1.serializers import CustomUserSerializer

from .tag import TagSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                mediatype, imgstr = data.split(';base64,')
            except ValueError:
                raise serializers.ValidationError(
                    'The submitted data is not a base64 string'
                )
            extension = mediatype.split('/')[-1]

            data = ContentFile(
                base64.b64decode(imgstr),
                name='recipe.' + extension
            )

        return super().to_internal_value(data)


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


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        allow_null=False,
        required=True
    )
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
            'image',
            'name',
            'text',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
        )

    def __check_related_ingredients(self, ingredients_data):
        if not ingredients_data:
            return

        ingredients_ids = Ingredient.objects.all().values_list('id', flat=True)
        for ingredient in ingredients_data:
            if ingredient['id'] not in ingredients_ids:
                raise serializers.ValidationError(
                    f'There is no ingrediet with id={ingredient["id"]}'
                )

    def __check_related_tags(self, tags_data):
        if not tags_data:
            return

        tags_ids = Tag.objects.all().values_list('id', flat=True)
        for tag in tags_data:
            if tag.id not in tags_ids:
                raise serializers.ValidationError(
                    f'There is no tag with id={tag["id"]}'
                )

    def __save_related_ingredients(self, ingredients_data, obj, update=False):
        if not ingredients_data:
            return

        if not update:
            for ingredient_data in ingredients_data:
                obj.ingredients.add(
                    ingredient_data['id'],
                    through_defaults={'amount': ingredient_data['amount']}
                )
        else:
            obj.ingredientamount_set.all().delete()
            for ingredient_data in ingredients_data:
                obj.ingredients.add(
                    ingredient_data['id'],
                    through_defaults={'amount': ingredient_data['amount']}
                )

    def __save_related_tags(self, tags_data, obj):
        if tags_data:
            obj.tags.set(tags_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredientamount_set', None)
        tags_data = validated_data.pop('tags', None)

        recipe = Recipe(
            author=self.context.get('request').user,
            **validated_data
        )
        recipe.full_clean()
        self.__check_related_ingredients(ingredients_data)
        self.__check_related_tags(tags_data)
        recipe.save()
        self.__save_related_ingredients(ingredients_data, recipe)
        self.__save_related_tags(tags_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredientamount_set', None)
        tags_data = validated_data.pop('tags', None)

        self.__check_related_ingredients(ingredients_data)
        self.__check_related_tags(tags_data)

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.pop('name', instance.name)
        instance.text = validated_data.pop('text', instance.text)
        instance.cooking_time = validated_data.pop(
            'cooking_time', instance.cooking_time
        )
        instance.save()
        self.__save_related_ingredients(
            ingredients_data,
            instance,
            update=True
        )
        self.__save_related_tags(tags_data, instance)

        return instance


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(
        allow_null=False,
        required=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        allow_null=False,
        required=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
