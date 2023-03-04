from typing import (
    Any,
    Dict
)

from django_filters import rest_framework as df_filters

from recipes.models import (
    Recipe,
    Tag
)

BINARY_CHOISES = {
    0: False,
    1: True,
}


class RecipeFilter(df_filters.FilterSet):
    author = df_filters.NumberFilter(
        field_name='author__id',
    )
    is_favorited = df_filters.NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = df_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = df_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        fields = [
            'author',
            'tags',
        ]
        model = Recipe

    def get_is_favorited(self, queryset, name, value):
        return self.__get_on_condition(queryset, name, value, BINARY_CHOISES)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return self.__get_on_condition(queryset, name, value, BINARY_CHOISES)

    def __get_on_condition(
        self,
        queryset,
        name,
        value,
        choises: Dict[int, Any]
    ):
        '''
        Returns `QuerySet` that matches boolean condition.

        The filter field `name` is expected to be annotated
        in the `queryset` in the according ViewSet.
        '''
        choise_val = choises.get(value, None)
        if choise_val is None:
            return queryset

        return queryset.filter(**{name: choise_val})
