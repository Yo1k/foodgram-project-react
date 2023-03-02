from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class CustomUserAdmin(UserAdmin):
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
        'email',
        'username',
    )


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.User, CustomUserAdmin)
