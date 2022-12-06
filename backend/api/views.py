from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters
from rest_framework import views
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.models import (Tag, Recipe, Ingredient, Subscribe, Favorite,
                            IngredientRecipe, Cart)
from users.models import User
from .filtres import RecipeFilters
from .permissions import IsAuthorOrReadOnly
from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          SubscribeSerializer,
                          RecipeListSerializer, CustomUserCreateSerializer,
                          ShoppingCartSerializer, FavoriteSerializer)


class TagViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей тэгов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки модели продуктов.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CreateUserViewSet(UserViewSet):
    """
    Вьюсет обработки моделей пользователя.
    """
    serializer_class = CustomUserCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей подписок.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Метод создания подписки.
        """
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления подписок.
        """
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_class = RecipeFilters
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """
        Метод выбора сериализатора в зависимости от запроса.
        """
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeSerializer


class ShoppingCartAPIView(views.APIView):

    def post(self, request, id):
        user_id = request.user.id
        data = {'recipe': id, 'user': user_id}
        serializer = ShoppingCartSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        deleting_obj = Cart.objects.all().filter(
            user=user, recipe=recipe)
        deleting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadCart(viewsets.ModelViewSet):
    """
       Сохранение файла списка покупок.
       """
    permission_classes = [permissions.IsAuthenticated]

    def download(self, request):
        """
        Метод сохранения списка покупок в формате PDF.
        """
        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        final_list = {}
        for ingredient in ingredients:
            name = ingredient[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                final_list[name]['amount'] += ingredient[2]
        pdfmetrics.registerFont(
            TTFont('FreeSans', 'data/FreeSans.ttf', 'UTF-8'))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        c = canvas.Canvas(response)
        c.setFont('FreeSans', size=24)
        c.drawString(200, 800, 'Список ингредиентов')
        c.setFont('FreeSans', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            c.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                      f'{data["measurement_unit"]}'))
            height -= 25
        c.showPage()
        c.save()
        return response


class FavoriteAPIView(views.APIView):

    def post(self, request, id):
        user_id = request.user.id
        data = {"user": user_id, "recipe": id}
        serializer = FavoriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        deleting_obj = Favorite.objects.all().filter(user=user, recipe=recipe)
        if not deleting_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        deleting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
