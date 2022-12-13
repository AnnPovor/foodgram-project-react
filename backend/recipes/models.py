from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """ Модель ингредиента """
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента',
                            help_text='Напишите название ингредиента')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единицы измерения',
                                        help_text='Введите единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ Модель тега """
    name = models.CharField(max_length=200,
                            verbose_name='Название тега',
                            help_text='Выберите название тега')
    color = ColorField(format='hexa',
                       verbose_name='Цвет тега',
                       help_text='Выберите цвет тега')
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Тег',
                            help_text='Введите тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель рецептов """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор',
                               help_text='Выберите автора рецепта')
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта',
                            help_text='Напишите название рецепта')
    text = models.TextField(verbose_name='Описание рецепта',
                            help_text='Напишите описание рецепта')

    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='IngredientRecipe',
                                         verbose_name='Ингредиенты в рецепте',
                                         help_text='Выберите ингредиенты')

    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время готовки',
                                       help_text='Поставьте время готовки'
                                       )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тег рецепта',
                                  help_text='Выберите тег для рецепта')

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Добавьте дату публикации')

    image = models.ImageField(
        'Изображение',
        upload_to='recipes/image')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель ингредиентов в рецепте"""
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredientrecipes',
                                   verbose_name='Продукты блюда',
                                   help_text='Выберите продукты для блюда'
                                   )

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredientrecipes',
                               verbose_name='Рецепт',
                               help_text='Выберите рецепт'
                               )

    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Количество должно быть больше одного'
            )
        ],
        verbose_name='Количество продукта',
        help_text='Введите количество продукта'
    )

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class Cart(models.Model):
    """
    Создание модели корзины.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты',
        help_text='Выберите рецепты для добавления в корзины'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Subscribe(models.Model):
    """
    Создание модели подписок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора для подписки'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_subscribe')
        ]

    def __str__(self):
        return f'{self.user} {self.following}'


class Favorite(models.Model):
    """
    Создание модели избранных рецептов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'
