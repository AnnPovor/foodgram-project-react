from rest_framework import viewsets

from recipes.models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей тэгов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
