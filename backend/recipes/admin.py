from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . import models


class FavoriteAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


class IngredientAmountAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_author_link',
    )
    list_filter = (
        'author__username',
        'name',
        'tags__name',
    )
    ordering = ['-pub_date', 'name']
    readonly_fields = (
        'get_favorite_count',
    )

    @admin.display(
        description=_('Author'),
    )
    def get_author_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.author.pk,)),
            obj.author.username
        ))

    
    @admin.display(
        description=_('Total count "In Favorite" for this recipe'),
    )
    def get_favorite_count(self, obj):
        return obj.favorite_set.count()


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.IngredientAmount, IngredientAmountAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
admin.site.register(models.Tag, TagAdmin)
