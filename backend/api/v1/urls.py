from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'v1'

router = DefaultRouter()

router.register(
    'tags',
    views.TagViewSet,
    basename='tags'
)

urlpatterns = [
    path('', include(router.urls)),
]