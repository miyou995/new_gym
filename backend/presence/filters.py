from decimal import Decimal
from django.db.models import Q
import django_filters
import django_filters.widgets
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Presence
# from abonnement.models import AbonnementClient

class PresenceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))

    
    class Meta:
        model = Presence
        fields = ['search', 'date_creation']

    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(id__icontains=value))

        print('Filtered queryset:', queryset)
        return queryset.distinct()
