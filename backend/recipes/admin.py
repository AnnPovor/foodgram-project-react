from django.contrib import admin

from .models import (Ingredient, Tag, Recipe, IngredientRecipe,
                     Cart, Subscribe, Favorite)

admin.site.register((Ingredient, Tag, Recipe, IngredientRecipe,
                     Cart, Subscribe, Favorite))
