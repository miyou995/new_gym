import django_filters
import django_filters.widgets
from .models import Creneau
from planning.models import Planning
from salle_activite.models import Salle 



class CalenderFilterCreneau(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
    activity__salle = django_filters.ModelChoiceFilter(queryset=Salle.objects.all(), label="Abonnement")
    class Meta:
        model = Creneau
        fields = ['planning','activity__salle']

  




