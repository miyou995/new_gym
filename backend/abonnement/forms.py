from django import forms
from django.contrib.auth import authenticate
import logging
from .models import AbonnementClient
from client.models import Client


logger = logging.getLogger(__name__)


class AbonnemetsClientModelForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
          model=AbonnementClient
          fields =(
                'start_date',
                'end_date',
               'client',
               'creneaux',
               'type_abonnement',
               
          )
    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)

        initial= kwargs.get('initial',{})
        client_pk=initial.get('client_pk')
        if client_pk :
            try :
                initial['client']=Client.objects.get(pk=client_pk)
                print("work ftom tryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                # initial['abonnement_client']=AbonnementClient.objects.filter(client=client_pk)
            except Client.DoesNotExist:
                pass
        kwargs['initial']=initial
        super(AbonnemetsClientModelForm,self).__init__(*args,**kwargs)


        self.fields['client'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['creneaux'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['type_abonnement'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['start_date'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }