import django_filters
import django_filters.widgets
from .models import Abonnement
from creneau.models import Creneau

from planning.models import Planning
from salle_activite.models import Salle 



class CalenderFilter(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
    abonnement  = django_filters.ModelChoiceFilter(queryset=Abonnement.objects.all(), label="Abonnement",  method='filter_by_abonnement_salles')
    class Meta:
        model = Creneau
        fields = ['planning', 'abonnement']

    def filter_by_abonnement_salles(self, queryset, name, value):
        # print('VALUE of aB', value)
        # print('Queryset Before', queryset.count())
        if value:
            salles = value.salles.all()
            # print('les salees', salles)
            # print('value*********', value)
            # queryset = queryset.filter(activity__salle__abonnements=value)
            queryset = queryset.filter(activity__salle__abonnements=value)
            

            # print("queryset----------------",queryset)
            # for creneau in queryset:

                # print('creneau-----)',creneau)
                # print('creneau DAY-----)',creneau.day)
        return queryset




