from django.db.models import Q
import django_filters
import django_filters.widgets
from abonnement.models import Abonnement, AbonnementClient



class AbonnementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    
    class Meta:
        model = Abonnement
        fields = ['search' ]


    
    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(name=value) |  Q(id=value) )
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(name__icontains=value)   | Q(type_of__icontains=value) )


        print('Filtered queryset:', queryset)
        return queryset.distinct()