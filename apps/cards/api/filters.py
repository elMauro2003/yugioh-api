import django_filters
from apps.cards.models import Card
from django.db.models import Q

class CardFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')
    race = django_filters.CharFilter(lookup_expr='icontains')
    attribute = django_filters.CharFilter(lookup_expr='icontains')
    archetype = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.NumberFilter()
    atk = django_filters.NumberFilter()
    defense = django_filters.NumberFilter()
    scale = django_filters.NumberFilter()
    linkval = django_filters.NumberFilter()
    linkmarkers = django_filters.CharFilter(lookup_expr='icontains')
    sort = django_filters.OrderingFilter(
        fields=(
            ('atk', 'atk'),
            ('defense', 'defense'),
            ('name', 'name'),
            ('type', 'type'),
            ('level', 'level'),
        )
    )

    class Meta:
        model = Card
        fields = [
            'name', 'type', 'race', 'attribute', 'archetype', 
            'level', 'atk', 'defense', 'scale', 'linkval', 'linkmarkers'
        ]

    def filter_queryset(self, queryset):
        ordering = self.data.get('sort', None)
        if ordering in ['atk', '-atk', 'defense', '-defense', 'level', '-level']:
            queryset = queryset.exclude(Q(type='Trap Card') | Q(type='Spell Card'))
        return super().filter_queryset(queryset)