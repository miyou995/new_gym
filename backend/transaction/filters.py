# products/filters.py
from decimal import Decimal
from django.db.models import Q
import django_filters
import django_filters.widgets
from .models import Paiement,RemunerationProf,Remuneration


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Paiement
        fields = ['search', 'date_creation', ]


    
    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id=value) | Q(abonnement_client__type_abonnement=value) )
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(id__icontains=value)  )


        print('Filtered queryset:', queryset)
        return queryset.distinct()
    

class PersonnelFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Remuneration
        fields = ['search', 'date_creation', ]

    def  universal_search(self, queryset, name, value): 
        print('YESS FOR FILTER', value)
        print('YESS FOR queryset', queryset)
        
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id = value) | Q(nom= value) )

        print('YESS AFTER FILTERING queryset', queryset)
        return queryset.distinct()
                                                                    
     

class CoachFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search',label="")
    date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        
        model = RemunerationProf
        fields = ['search', 'date_creation', ]

    def  universal_search(self, queryset, name, value): 
        print('YESS FOR FILTER', value)
        print('YESS FOR queryset', queryset)
        
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id = value) | Q(coach= value) )

        print('YESS AFTER FILTERING queryset', queryset)    
        return queryset.distinct()
    