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
router.register(
    'recipes',
    views.RecipeViewSet,
    basename='recipes'
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

urlpatterns = [
    path('', include(router.urls)),
]
