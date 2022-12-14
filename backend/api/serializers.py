from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Subscribe, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователей"""

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')

    @transaction.atomic
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomUserSerializer(UserSerializer):
    """Сериализатор профиль пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'id',
                  'last_name')


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
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта"""
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user,
                                       recipe__id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user,
                                   recipe__id=obj.id).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта"""
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(many=True,
                                          source='ingredientrecipes')
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')

    def validate(self, data):
        ingredients = data['ingredientrecipes']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты должны быть уникальными!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиента должно быть больше нуля!'
                })

        tags = data['tags']
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать хотя бы один тэг!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Тэги должны быть уникальными!'
                })
            tags_list.append(tag)
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть больше 0!'
            })
        return data

    def create_bulk(self, ingredients, recipe):
        IngredientRecipe.objects.bulk_create([IngredientRecipe(
            recipe=recipe, ingredient=ingredient['id'],
            amount=ingredient['amount'])
            for ingredient in ingredients])

    @transaction.atomic
    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    @transaction.atomic
    def create(self, validated_data):
        """
        Метод создания рецептов.
        """
        ingredients = validated_data.pop('ingredientrecipes')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(tags_data, recipe)
        self.create_bulk(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Метод редактирования рецептов.
        """
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_bulk(validated_data.pop('ingredientrecipes'), instance)
        self.create_tags(validated_data.pop('tags'), instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор списка избранного"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'error': 'Рецепт уже есть в избранном!'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SimpleRecipeSerializer(
            instance.recipe, context=context).data


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для упрощенного отображения модели рецептов.
    """
    class Meta:
        """
        Мета параметры сериализатора упрощенного
        отображения модели рецептов.
        """
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'id',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """
        Метод обработки параметра is_subscribed подписок.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=request.user,
                                        following__id=obj.id).exists()

    def get_recipes_count(self, obj):
        """Определение количества рецептов автора"""
        return Recipe.objects.filter(author__id=obj.id).count()

    def get_recipes(self, obj):
        """Получение данных рецептов автора,
        в зависимости от параметра recipes_limit."""

        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(author__id=obj.id)[:recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id)
        return SimpleRecipeSerializer(queryset, many=True).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Cart.objects.filter(user=user,
                               recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже добавлен в список покупок'})
        return data
