from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserViewSet, DownloadCart, FavoriteAPIView,
                    IngredientViewSet, RecipeViewSet, ShoppingCartAPIView,
                    SubscribeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CreateUserViewSet, basename='users')

urlpatterns = [
    path('recipes/<int:id>/favorite/', FavoriteAPIView.as_view(),
         name='favorite'),
    path('recipes/<int:id>/shopping_cart/',
         ShoppingCartAPIView.as_view(),
         name='shopping_cart'),
    path('recipes/download_shopping_cart/',
         DownloadCart.as_view({'get': 'download'}),
         name='download_shopping_cart'),
    path('users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    ]
