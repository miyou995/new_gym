from django import forms
from django.urls import reverse
from creneau.models import Creneau
from client.models import Client
from presence.models import Presence
from django.utils.translation import gettext_lazy as _
from abonnement.models import AbonnementClient


class PresenceManuelleModelForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    class Meta:
        model  = Presence
        fields= ('client',
                'abc',
                'creneau',
                'hour_entree',
                'hour_sortie',
                'date',
                'note',
                 )
        widgets = {
           
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour_entree': forms.TimeInput(attrs={'type': 'time'}),
            'hour_sortie': forms.TimeInput(attrs={'type': 'time'})
        }
      
    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)

        initial= kwargs.get('initial',{})
        client_pk=initial.get('client_pk')
        if client_pk :
            try :
                initial['client']=Client.objects.get(pk=client_pk)
                # initial['abonnement_client']=AbonnementClient.objects.filter(client=client_pk)
            except Client.DoesNotExist:
                pass
        kwargs['initial']=initial
        super(PresenceManuelleModelForm,self).__init__(*args,**kwargs)
        

        self.fields["creneau"].widget.attrs.update({'id':'creneauSelectId'})

        self.fields["abc"].widget.attrs.update({'id' : 'abcSelectId',
            "hx-get": reverse('creneau:abc_creneau_view'),
            "hx-target":"#creneauSelectId",
            "hx-swap" : "innerHTML",
            "hx-trigger": "change, referesh_creneaux from:body delay:100",
            "hx-include":"[name='abc'] , [name='client']",
            })
        self.fields["client"].widget.attrs.update({
          
            "hx-get": reverse('abonnement:abc_htmx_view'),
            "hx-target":"#abcSelectId",
            "hx-swap" : "innerHTML",
            "hx-trigger": "change",
            "hx-include":"[name='client']",
            })

        self.fields["abc"].queryset = AbonnementClient.objects.none()
        if 'client' in self.data:
            client = self.data.get('client')
            self.fields['abc'].queryset = AbonnementClient.objects.filter(client=client)
        elif self.instance.pk:
            self.fields['abc'].queryset = self.instance.client.abonnement_client

        
        self.fields["creneau"].queryset = AbonnementClient.objects.none()
        if 'abc' in self.data:
            abc = self.data.get('abc')
            print("abc = self.data.get('abc')------------",abc)
            self.fields['creneau'].queryset = Creneau.objects.filter(abonnements__id= abc)
            print("self.fields['creneau'].queryse)------------\n \n \n ",self.fields['creneau'].queryset)

        elif self.instance.pk:
            self.fields['creneau'].queryset = self.instance.client.abonnements

      
        self.fields['client'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['abc'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['hour_entree'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['hour_sortie'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['creneau'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }


