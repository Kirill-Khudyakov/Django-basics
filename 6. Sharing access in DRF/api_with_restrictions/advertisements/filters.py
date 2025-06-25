from django_filters import rest_framework as filters
from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    is_favorite = filters.BooleanFilter(method='filter_is_favorite')

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']


    def filter_is_favorite(self, quereset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return quereset.none() if value else quereset
        if value:
            return quereset.filter(favorited_by__user=user)
        else:
            return quereset.exclude(favorited_by__user=user)
        

class FavoriteFilter(filters.FilterSet):
    """Фильтр для избранного"""

    user = filters.NumberFilter(field_name='user__id')

    
    class Meta:
        model = Favorite
        fields = ['user']