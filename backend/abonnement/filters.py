import django_filters
import django_filters.widgets
from .models import Abonnement, AbonnementClient
from creneau.models import Creneau
from django.shortcuts import get_object_or_404
from planning.models import Planning
from salle_activite.models import Salle 



class CalenderFilter(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(queryset=Planning.objects.all(), label="Planning")
    type_abonnement  = django_filters.ModelChoiceFilter(queryset=Abonnement.objects.all(),
                                                    label="Abonnement", 
                                                      method='filter_by_abonnement_salles',
                                                      required=False)
    class Meta:
        model = Creneau
        fields = ['planning', 'type_abonnement']
        
    def __init__(self, *args, **kwargs):
        super(CalenderFilter, self).__init__(*args, **kwargs)
        items_data= "\n".join(f'{key} {value}' for key, value in self.data.items())

        print('SELF.data.items---------------------------------', items_data)
        
        if 'abc_id' in self.data:
            print('abc_id=========================', self.data.get('abc_id'))
            abc_id = int(self.data.get('abc_id'))
            abonnement_client=get_object_or_404(AbonnementClient, pk=abc_id)
            abonnement = Abonnement.objects.get(id=abonnement_client.type_abonnement.id)
            # self.form.initial['type_abonnement'] = abonnement 
            self.data = self.data.copy()  # Make self.data mutable
            self.data['type_abonnement'] = abonnement.id
            # print('new selected abonnement', abonnement)
            print("-----------------\n \n \n self.form.initial['type_abonnement'] \n \n", self.form.initial.get('type_abonnement', None))
        else:
            print("NO ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
        # self.form.initial['planning'] = Planning.objects.get(is_default=True)
        
                
    # def __init__(self, *args, **kwargs):
    #     super(CalenderFilter, self).__init__(*args, **kwargs)
    #     print('SELF.data.items---------------------------------', self.data.items())
    #     if 'abc_id' in self.data:
    #         print('abc_id=========================', self.data.get('abc_id'))
    #         try:
    #             abc_id = int(self.data.get('abc_id'))
    #             abonnement_client=get_object_or_404(AbonnementClient, pk=abc_id)
    #             self.form.initial['type_abonnement'] = Abonnement.objects.get(id=abonnement_client.type_abonnement.id)
    #         except (ValueError, Abonnement.DoesNotExist):
    #             print('new selected abonnement')
    #             pass
    #     self.form.initial['planning'] = Planning.objects.get(is_default=True)

        
        
        
    def filter_by_abonnement_salles(self, queryset, name, value):
        if value:
            salles = value.salles.all()
            queryset = queryset.filter(activity__salle__abonnements=value)
        return queryset




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
#             queryset = Creneau.objects.filter(activity__salle__abonnements=value)
#         return queryset
