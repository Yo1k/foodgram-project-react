from django.db.models import Sum
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    IngredientAmount,
    Recipe
)

from ..exceptions import ShopCartActionError
from ..serializers import RecipeMinifiedSerializer

# Constants with errors messages:
REPITE_SHOPPING_CART_ACTION_MESSAGE = _(
    'You are trying repeatedly add (delete) the same recipe to shopping cart'
)


class ShoppingCartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeMinifiedSerializer

    def get_queryset(self):
        return Recipe.objects.all()

    @action(detail=False)
    def download_shopping_cart(self, request):
        recipes_in_cart_ids = (
            Recipe.objects
            .filter(shoppingcart__user=self.request.user)
            .values('id')
        )

        ingrds_amounts = (
            IngredientAmount.objects.filter(recipe__in=recipes_in_cart_ids)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name', 'ingredient__measurement_unit')
        )

        response = HttpResponse(
            'Shopping list:\n',
            content_type='text/plain; charset=UTF-8',
            status=status.HTTP_200_OK
        )
        for num, ingrd_amount in enumerate(ingrds_amounts, start=1):
            # Example: 1. Ingredient (unit) - 100
            response.write(
                f'{num}. {ingrd_amount["ingredient__name"]} '
                f'({ingrd_amount["ingredient__measurement_unit"]}) \u2014 '
                f'{ingrd_amount["total_amount"]}\n'
            )

        response['Content-Length'] = response.tell()
        response['Content-Disposition'] = (
            'attachment; filename=shopping_list.txt'
        )
        return response

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        instance = self.get_object()

        is_in_shopping_cart = instance.shoppingcart_set.filter(
            user=request.user
        ).exists()

        if request.method == 'POST':
            if not is_in_shopping_cart:
                instance.shoppingcart_set.create(
                    recipe=instance,
                    user=self.request.user
                )
            else:
                raise ShopCartActionError(REPITE_SHOPPING_CART_ACTION_MESSAGE)
            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        if request.method == 'DELETE':
            if is_in_shopping_cart:
                instance.shoppingcart_set.get(
                    recipe=instance,
                    user=self.request.user
                ).delete()
            else:
                raise ShopCartActionError(REPITE_SHOPPING_CART_ACTION_MESSAGE)

            return Response(status=status.HTTP_204_NO_CONTENT)

        assert False
