# Generated by Django 2.2.19 on 2022-11-21 04:18

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите название ингредиента', max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Введите единицы измерения', max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Поставьте количество', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('ingredients', models.ForeignKey(help_text='Выберите продукты для блюда', on_delete=django.db.models.deletion.CASCADE, related_name='ingredientrecipes', to='recipes.Ingredient', verbose_name='Продукты блюда')),
            ],
            options={
                'verbose_name': 'Ингредиенты рецепта',
                'verbose_name_plural': 'Ингредиенты рецептов',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Выберите название тега', max_length=200, verbose_name='Название тега')),
                ('color', colorfield.fields.ColorField(default='#FFFFFFFF', help_text='Выберите цвет тега', image_field=None, max_length=18, samples=None, verbose_name='Цвет тега')),
                ('slug', models.SlugField(help_text='Введите тег', max_length=200, unique=True, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите название рецепта', max_length=200, verbose_name='Название рецепта')),
                ('text', models.TextField(help_text='Напишите описание рецепта', verbose_name='Описание рецепта')),
                ('cooking_time', models.IntegerField(help_text='Поставьте время готовки', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время готовки')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Добавьте дату публикации', verbose_name='Дата публикации')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Изображение')),
                ('author', models.ForeignKey(help_text='Выберите автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(help_text='Выберите ингредиенты', related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингредиенты в рецепте')),
                ('tags', models.ManyToManyField(help_text='Выберите тег для рецепта', related_name='recipes', to='recipes.Tag', verbose_name='Тег рецепта')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredientrecipes', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]
