from rest_framework import serializers

from recipes.models import Tag, Ingredient, IngredientRecipe, Recipe


class TagSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели тегов.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', 'id')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте с количеством"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
#
#
# class RecipeSerializer(serializers.ModelSerializer):
#     image = Base64ImageField()
#     tags = TagSerializer(read_only=True, many=True)
#     author = UserSerializer(read_only=True)
#     ingredients = IngredientRecipeSerializer(
#         source='ingredientrecipes',
#         many=True,
#         read_only=True,
#     )
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
#                   'is_in_shopping_cart', 'name', 'image', 'text',
#                   'cooking_time')
#
#     def get_is_favorited(self, obj):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         return FavoriteRecipe.objects.filter(recipe=obj,
#                                              user=request.user).exists()
#
#     def get_is_in_shopping_cart(self, obj):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         return ShoppingList.objects.filter(recipe=obj,
#                                            user=request.user).exists()
#
#     def validate_ingredients(self, value):
#         ingredients_list = []
#         ingredients = value
#         for ingredient in ingredients:
#             if ingredient['amount'] < 1:
#                 raise serializers.ValidationError(
#                     'Количество ингредиентов должно быть больше или равным 1!')
#             id_to_check = ingredient['ingredient']['id']
#             ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
#             if not ingredient_to_check.exists():
#                 raise serializers.ValidationError(
#                     'Данного продукта нет в базе!')
#             if ingredient_to_check in ingredients_list:
#                 raise serializers.ValidationError(
#                     'Данные продукты повторяются в рецепте!')
#             ingredients_list.append(ingredient_to_check)
#         return value
#
#     def create_ingredients(self, ingredients, recipe):
#         for ingredient in ingredients:
#             IngredientRecipe.objects.create(
#                 recipe=recipe,
#                 ingredient_id=ingredient.get('id'),
#                 amount=ingredient.get('amount'),
#             )
#
#     def create(self, validated_data):
#         image = validated_data.pop('image')
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(image=image, **validated_data)
#         tags_data = self.initial_data.get('tags')
#         recipe.tags.set(tags_data)
#         self.create_ingredients(ingredients_data, recipe)
#         return recipe
#
#     def update(self, instance, validated_data):
#         instance.image = validated_data.get('image', instance.image)
#         instance.name = validated_data.get('name', instance.name)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cooking_time = validated_data.get(
#             'cooking_time', instance.cooking_time
#         )
#         instance.tags.clear()
#         tags_data = self.initial_data.get('tags')
#         instance.tags.set(tags_data)
#         IngredientRecipe.objects.filter(recipe=instance).all().delete()
#         self.create_ingredients(validated_data.get('ingredients'), instance)
#         instance.save()
#         return instance
