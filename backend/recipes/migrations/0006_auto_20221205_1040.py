# Generated by Django 2.2.19 on 2022-12-05 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20221128_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ('-id',), 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]
