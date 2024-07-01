from decimal import Decimal
from django.db.models import Q
import django_filters
import django_filters.widgets
from .models import Client,Coach,Personnel


class ClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    # date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    
    class Meta:
        model = Client
        fields = ['search']

    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id=value) | Q(last_name=value) | Q(first_name=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(last_name__icontains=value)  | Q(first_name__icontains=value)  | Q(id__icontains=value))

        print('Filtered queryset:', queryset)
        return queryset.distinct()
   




class CoachFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    # date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Coach
        fields = ['search']

    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id=value) | Q(last_name=value) | Q(first_name=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(last_name__icontains=value)  | Q(first_name__icontains=value)  | Q(id__icontains=value))

        print('Filtered queryset:', queryset)
        return queryset.distinct()

class PersonnelFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    # date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Personnel
        fields = ['search']

    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id=value) | Q(last_name=value) | Q(first_name=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(last_name__icontains=value)  | Q(first_name__icontains=value)  | Q(id__icontains=value))

        print('Filtered queryset:', queryset)
        return queryset.distinct()
    