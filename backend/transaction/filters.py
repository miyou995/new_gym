# products/filters.py
from decimal import Decimal
from django.db.models import Q
import django_filters
import django_filters.widgets
from .models import Paiement,RemunerationProf,Remuneration,Autre


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
            queryset = queryset.filter(Q(abonnement_client__client__id=value) | Q(abonnement_client__type_abonnement=value) )
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(abonnement_client__client__id__icontains=value)  )


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
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(nom__last_name__icontains=value)  )

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
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(coach__last_name__icontains=value)  )

        print('YESS AFTER FILTERING queryset', queryset)    
        return queryset.distinct()
    
class AutreTransactionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search',label="")
    date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        
        model = Autre
        fields = ['search', 'date_creation' ]

    def  universal_search(self, queryset, name, value): 
        print('YESS FOR FILTER', value)
        print('YESS FOR queryset', queryset)
        
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(id = value) | Q(name= value) )
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(name__icontains=value)  )

        print('YESS AFTER FILTERING queryset', queryset)    
        return queryset.distinct()
    