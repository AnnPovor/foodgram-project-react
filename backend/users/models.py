from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создание кастомной модели пользователя"""
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Введите логин пользователя')
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту пользователя')
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите имя пользователя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя')
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на данного пользователя',
        help_text='Отметьте для подписки на данного пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
