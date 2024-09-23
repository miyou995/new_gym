import django_filters
import django_filters.widgets
from .models import Abonnement
from creneau.models import Creneau

from planning.models import Planning
from salle_activite.models import Salle 



# class CalenderFilter(django_filters.FilterSet):
#     planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
#     abonnement  = django_filters.ModelChoiceFilter(queryset=Abonnement.objects.all(),
#                                                     label="Abonnement", 
#                                                       method='filter_by_abonnement_salles',
#                                                       required=False)
#     class Meta:
#         model = Creneau
#         fields = ['planning', 'abonnement']

#     def filter_by_abonnement_salles(self, queryset, name, value):
#         if value:
#             salles = value.salles.all()
#             queryset = queryset.filter(activity__salle__abonnements=value)
#         return queryset




class CalenderFilter(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
    abonnement  = django_filters.ModelChoiceFilter(queryset=Abonnement.objects.all(),
                                                    label="Abonnement", 
                                                      method='filter_by_abonnement_salles',
                                                      required=False)
    class Meta:
        model = Creneau
        fields = ['planning', 'abonnement']

    def filter_by_abonnement_salles(self, queryset, name, value):
        if value:
            queryset = Creneau.objects.filter(activity__salle__abonnements=value)
        return queryset
