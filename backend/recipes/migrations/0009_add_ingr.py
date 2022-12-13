import json

from django.db import migrations

file = open('./data/ingredients.json', encoding="utf-8")
INITIAL_INGREDIENTS = json.load(file)


def add_ingr(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    for ingredient in INITIAL_INGREDIENTS:
        new_ingredient = Ingredient(**ingredient)
        new_ingredient.save()


def remove_ingr(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    for ingredient in INITIAL_INGREDIENTS:
        Ingredient.objects.get(name=ingredient['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingr,
            remove_ingr
        )
    ]
