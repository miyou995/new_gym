from django.db.models import Q
import django_filters
import django_filters.widgets
from .models import Creneau
from planning.models import Planning
from salle_activite.models import Activity 



class CalenderFilter(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
    activity = django_filters.ModelChoiceFilter(queryset=Activity.objects.all(), label="Activity")
    class Meta:
        model = Creneau
        fields = ['planning','activity']

  




