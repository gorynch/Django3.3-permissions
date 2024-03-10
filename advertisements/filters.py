from django_filters import rest_framework as filters
from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'user_favorites']

    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
