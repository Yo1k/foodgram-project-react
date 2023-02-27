from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'v1'

router = DefaultRouter()

router.register(
    'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
)
# Order is important for the same `prefix` or it is bug:
# 'shopping_cart' with GET method are not found in the case
# if it is placed after 'recipes' (btw POST and DELETE works properly)
router.register(
    'recipes',
    views.FavoriteRecipesViewSet,
    basename='favorites'
)
router.register(
    'recipes',
    views.ShoppingCartViewSet,
    basename='shopping_cart'
)
router.register(
    'recipes',
    views.RecipeViewSet,
    basename='recipes'
)
router.register(
    'tags',
    views.TagViewSet,
    basename='tags'
)
router.register(
    'users',
    views.SubscriptionViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('', include(router.urls)),
]
