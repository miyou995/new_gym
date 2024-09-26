from django import forms
from django.contrib.auth import authenticate
import logging
from .models import AbonnementClient


logger = logging.getLogger(__name__)


class AbonnementClientRestTempForm(forms.ModelForm):
    class Meta:
        model = AbonnementClient
        fields = ( "presence_quantity",)

class AbonnementClientRestPaiementForm(forms.ModelForm):
    class Meta:
        model = AbonnementClient
        fields = ( "reste",)

# class AbonnemetsClientModelForm(forms.ModelForm):
#     client = forms.ModelChoiceField(queryset=Client.objects.all())

#     class Meta:
#           model=AbonnementClient
#           fields =(
#                 'start_date',
#                 'end_date',
#                'client',
#                'creneaux',
#                'type_abonnement',
               
#           )
#     def __init__(self, ticket=None, *args, **kwargs):   
#         super().__init__(*args, **kwargs)

#         initial= kwargs.get('initial',{})
#         client_pk=initial.get('client_pk')
#         if client_pk :
#             try :
#                 initial['client']=Client.objects.get(pk=client_pk)
#                 print("work ftom tryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
#                 # initial['abonnement_client']=AbonnementClient.objects.filter(client=client_pk)
#             except Client.DoesNotExist:
#                 pass
#         kwargs['initial']=initial
#         super(AbonnemetsClientModelForm,self).__init__(*args,**kwargs)


#         self.fields['client'].error_messages = {
#             'required': 'veuillez choisir.',
#             'invalid': 'Custom error message for field1 is invalid.',
          
#         }
#         self.fields['creneaux'].error_messages = {
#             'required': 'veuillez choisir.',
#             'invalid': 'Custom error message for field2 is invalid.',
#         }
#         self.fields['type_abonnement'].error_messages = {
#             'required': 'veuillez choisir.',
#             'invalid': 'Custom error message for field2 is invalid.',
#         }
#         self.fields['start_date'].error_messages = {
#             'required': 'veuillez choisir.',
#             'invalid': 'Custom error message for field2 is invalid.',
#         }


# from datetime import  timedelta

# from django import forms
# from .models import AbonnementClient
# from creneau.models import Creneau

# class UpdateAbonnementClientForm(forms.ModelForm):
#     # Define any additional fields that are not part of the model, if necessary
#     event_pk = forms.ModelMultipleChoiceField(
#         queryset=Creneau.objects.all(),
#         widget=forms.CheckboxSelectMultiple,  # You can adjust the widget as per your needs
#         required=True,
#         label="Select Events"
#     )
#     today = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

#     class Meta:
#         model = AbonnementClient
#         fields = ['type_abonnement', 'start_date', 'end_date']

#     def __init__(self, *args, **kwargs):
#         super(UpdateAbonnementClientForm, self).__init__(*args, **kwargs)
#         # If needed, set an initial value for `today`
#         self.fields['today'].initial = kwargs.get('initial', {}).get('today', None)

#     def save(self, commit=True):
#         abonnement_client = super().save(commit=False)  # Get the AbonnementClient instance
        
#         # Get the event primary keys and fetch the Creneaux instances
#         selected_creneaux = self.cleaned_data['event_pk']
        
#         # Update abonnement_client fields
#         abonnement_client.start_date = self.cleaned_data['today']
#         abonnement_client.end_date = abonnement_client.start_date + timedelta(days=30)

#         if commit:
#             abonnement_client.save()  # Save the AbonnementClient instance first
#             abonnement_client.creneaux.set(selected_creneaux)  # Update many-to-many field

#         return abonnement_client



