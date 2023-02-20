from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from .validators import color_hex_validator

# The length of text used in `__str__`
LENGTH_STR = 15


User = get_user_model()


class Ingredient(models.Model):
    measurement_unit = models.CharField(
        _('measurement unit'),
        max_length=200,
    )
    name = models.CharField(
        _('name'),
        max_length=200,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (
            f'name={self.name[:LENGTH_STR]}, '
            f'measurement_unit={self.measurement_unit[:LENGTH_STR]}'
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE
    )
    cooking_time = models.PositiveSmallIntegerField(
        _('cooking time'),
        validators=[MinValueValidator(1),]
    )
    # image = ... # SKTODO
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name=_('ingredients')
    )
    name = models.CharField(
        _('name'),
        max_length=200,
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('tags')
    )
    text = models.TextField(
        _('description')
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f'name={self.name[:LENGTH_STR]}'


class IngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        validators=[MinValueValidator(1),]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name=_('ingredient')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )

    def __str__(self) -> str:
        return (
            f'recipe_id={self.recipe}, '
            f'ingredient_id={self.ingredient}, '
            f'amount={self.amount}'
        )


class Tag(models.Model):
    color = models.CharField(
        _('HEX color'),
        blank=True,
        max_length=7,
        null=True,
        unique=True,
        validators=[color_hex_validator,]
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        _('unique slug'),
        blank=True,
        max_length=200,
        null=True,
        unique=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'name={self.name}'


# class ShoppingCart(models.Model):
#     pass


# class Favorite(models.Model):
#     pass
