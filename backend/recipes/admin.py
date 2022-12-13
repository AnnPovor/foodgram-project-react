from django.contrib import admin

from users.models import User

from .models import (Cart, Favorite, Ingredient, IngredientRecipe, Recipe,
                     Subscribe, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time',
                    'id', 'count_favorite', 'pub_date')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    list_filter = ('name', 'author', 'tags')

    def count_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    count_favorite.short_description = 'Число добавлении в избранное'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    search_fields = ('recipe',)
    empty_value_display = '-пусто-'
    list_filter = ('recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'id')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email')
