from decimal import Decimal
from django.db.models import Q
import django_filters
import django_filters.widgets
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Presence
# from abonnement.models import AbonnementClient

class CustomRangeWidget(django_filters.widgets.RangeWidget):
    template_name = "snippets/_custom_range_widget.html"


class PresenceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='universal_search', label="")
    date = django_filters.DateFromToRangeFilter(label="date", 
                                                lookup_expr='range', widget=CustomRangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Presence
        fields = ['search', 'date','creneau__activity','creneau__activity__salle','creneau']
        labels = {
           
            'creneau__activity': 'Activity',
            'creneau__activity__salle': 'Salle'
        }
    def __init__(self, *args, **kwargs):
        super(PresenceFilter, self).__init__(*args, **kwargs)

        self.form.fields['creneau__activity'].label = 'Activity'
        self.form.fields['creneau__activity__salle'].label = 'Salle'

    def universal_search(self, queryset, name, value):
        print('Filter value:', value)
        print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(abc__client=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(Q(abc__client=value))

        print('Filtered queryset:', queryset)
        return queryset.distinct()
