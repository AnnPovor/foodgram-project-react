from django_filters import rest_framework as django_filter
from recipes.models import Recipe
from rest_framework.filters import SearchFilter
from users.models import User


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilters(django_filter.FilterSet):
    """
    Настройка фильтров модели рецептов по:
    автору, тегам, подписке и нахождению в корозине.
    """
    author = django_filter.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filter.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filter.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filter.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset.all()
