from django.urls import (
    include,
    path
)

from .views import CustomUserViewSet

app_name = 'v1'


urlpatterns = [
    path(
        'users/',
        CustomUserViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'users/me/',
        CustomUserViewSet.as_view({'get': 'me'})
    ),
    path(
        'users/<int:id>/',
        CustomUserViewSet.as_view({'get': 'retrieve'})
    ),
    path(
        'users/set_password/',
        CustomUserViewSet.as_view({'get': 'set_password'})
    ),
    path(
        'auth/',
        include('djoser.urls.authtoken')
    ),
]
