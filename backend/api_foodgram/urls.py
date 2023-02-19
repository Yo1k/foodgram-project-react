from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.views import CustomUserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='Foodgram',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/users/',
        CustomUserViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'api/users/me/',
        CustomUserViewSet.as_view({'get': 'me'})
    ),
    path(
        'api/users/<int:id>/',
        CustomUserViewSet.as_view({'get': 'retrieve'})
    ),
    path(
        '/api/users/set_password/',
        CustomUserViewSet.as_view({'get': 'set_password'})
    ),
    path(
        'api/',
        include('djoser.urls.authtoken')
    ),
]

urlpatterns += [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
]