from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Paiement,Remuneration,Client,RemunerationProf,Personnel,Coach,Autre
from django.utils.translation import gettext_lazy as _
from abonnement.models import AbonnementClient


# class PaiementModelForm(forms.ModelForm):
#     amount = forms.IntegerField(required=False, label="Montant")
#     # Define the client field here without setting it up in the class body
#     client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)

#     class Meta:
#         model = Paiement
#         fields = ('client', 'abonnement_client', 'amount', 'notes')

#     def clean_amount(self):
#         amount = self.cleaned_data.get('amount')
#         if not amount:
#             raise forms.ValidationError(_('Veuillez renseigner ce champ'))
#         if amount < 0:
#             raise forms.ValidationError(_('Montant doit être supérieur à zéro'))
#         return amount

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         initial = kwargs.get('initial', {})
#         client_pk = initial.get('client_pk')

#         if client_pk:
#             try:
#                 client = Client.objects.get(pk=client_pk)
#                 initial['client'] = client
#                 self.fields['client'].queryset = Client.objects.filter(pk=client_pk)
#                 self.fields['client'].widget = forms.HiddenInput()

#             except Client.DoesNotExist:
#                 pass
        
#         kwargs['initial'] = initial
#         super(PaiementModelForm, self).__init__(*args, **kwargs)

#         # Set up the "abonnement_client" field as you did before
#         self.fields["abonnement_client"].widget.attrs.update({'id': 'abcSelectId'})
#         self.fields["client"].widget.attrs.update({
#             "hx-get": reverse('abonnement:abc_htmx_view'),
#             "hx-target": "#abcSelectId",
#             "hx-swap": "innerHTML",
#             "hx-trigger": "change,load",
#             "hx-include": "[name='client']",
#         })
#         self.fields["abonnement_client"].queryset = AbonnementClient.objects.none()

#         if 'client' in self.data:
#             client = self.data.get('client')
#             self.fields['abonnement_client'].queryset = AbonnementClient.objects.filter(client=client)
#         elif self.instance.pk:
#             self.fields['abonnement_client'].queryset = self.instance.client.abonnement_client

#         if client_pk:
#             abonnements = AbonnementClient.objects.filter(client__pk=client_pk)
#             self.fields['abonnement_client'].queryset = abonnements
#             self.fields['client'].widget = forms.HiddenInput()
#             if abonnements.exists():
#                 self.initial['abonnement_client'] = abonnements.last()

#         # Ensure no error modification on 'client' field since it's hidden
#         self.fields['client'].error_messages = {
#             'required': 'veuillez choisir.',
#             'invalid': 'Custom error message for field1 is invalid.',
#         }


class PaiementModelForm(forms.ModelForm):
    amount = forms.IntegerField(required=False, label="Montant")
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)

    class Meta:
        model = Paiement
        fields = ('client', 'abonnement_client', 'amount', 'notes')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)

        # Determine the client_pk either from initial or from the bound form data
        client_pk = initial.get('client_pk')
        if self.is_bound:
            # If the form is submitted, try to get the client from POST data, fallback to client_pk
            client_id = self.data.get('client', client_pk)
        else:
            client_id = client_pk

        # Configure the fields based on whether we have a specific client_id or not
        if client_id:
            try:
                client_obj = Client.objects.get(pk=client_id)
                # Restrict client field to a single client and hide it
                self.fields['client'].queryset = Client.objects.filter(pk=client_id)
                self.initial['client'] = client_obj
                self.fields['client'].widget = forms.HiddenInput()

                # Filter abonnements for the given client
                abonnements = AbonnementClient.objects.filter(client=client_obj)
                self.fields['abonnement_client'].queryset = abonnements
                if abonnements.exists():
                    self.initial['abonnement_client'] = abonnements.last()

            except Client.DoesNotExist:
                # If the client does not exist, just leave defaults
                pass
        else:
            # No specific client, so show all clients and no initial abonnements
            self.fields["abonnement_client"].queryset = AbonnementClient.objects.none()

        # Set widget attributes for HTMX
        self.fields["abonnement_client"].widget.attrs.update({'id': 'abcSelectId'})
        self.fields["client"].widget.attrs.update({
            "hx-get": reverse('abonnement:abc_htmx_view'),
            "hx-target": "#abcSelectId",
            "hx-swap": "innerHTML",
            "hx-trigger": "change,load",
            "hx-include": "[name='client']",
        })

        # Custom error messages for the client field
        self.fields['client'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError(_('Veuillez renseigner ce champ'))
        if amount < 0:
            raise forms.ValidationError(_('Montant doit être supérieur à zéro'))
        return amount

    
class Remuneration_PersonnelModelForm(forms.ModelForm):
    nom = forms.ModelChoiceField(queryset=Personnel.objects.all(),required=False)
    amount = forms.IntegerField(required=False,label="Montant")
    class Meta:
        model  = Remuneration
        fields = ('nom',
                'amount', 
                'notes',
                 )
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount :
            raise forms.ValidationError(_('Veuillez renseigner ce champ'))
        if amount < 0:
            raise forms.ValidationError(_('Montant doit être supérieur à zéro'))
        return amount
    
    
    def __init__(self, ticket=None, *args, **kwargs):   
        initial = kwargs.get('initial', {})
        personnel_pk = initial.get('personnel_pk')
        if personnel_pk:
            try:
                initial['nom'] = Personnel.objects.get(pk=personnel_pk)
            except Personnel.DoesNotExist:
                pass
        kwargs['initial'] = initial  # Update kwargs with the modified initial
        super(Remuneration_PersonnelModelForm, self).__init__(*args, **kwargs)

        self.fields['nom'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
            # Add more custom error messages for different errors if needed
        }
        self.fields['amount'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }


    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        if not nom:
                self.add_error('nom', _('veuillez choisir.'))
        return cleaned_data

 



class Remunération_CoachModelForm(forms.ModelForm):
    coach = forms.ModelChoiceField(queryset=Coach.objects.all())
    amount = forms.IntegerField(required=False, label="Montant")

    class Meta:
        model  = RemunerationProf
        fields = ('coach',
                'amount', 
                'notes',
                 )
   
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        coach_pk = initial.get('coach_pk')
        if coach_pk:
            try:
                initial['coach'] = Coach.objects.get(pk=coach_pk)
            except Coach.DoesNotExist:
                pass
        kwargs['initial'] = initial  # Update kwargs with the modified initial
        super(Remunération_CoachModelForm, self).__init__(*args, **kwargs)
        
        self.fields["coach"].widget.attrs.update()
        self.fields['coach'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
        }
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount :
            raise forms.ValidationError(_('Veuillez renseigner ce champ'))
        if amount < 0:
            raise forms.ValidationError(_('Montant doit être supérieur à zéro'))
        return amount
    
 
    

    

class Autre_TransactionForm(forms.ModelForm):
    amount = forms.IntegerField(required=False, label="Montant")
    

    class Meta:
        model  = Autre
        fields = ('name',
                'amount', 
                'notes',  
                 )
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount :
            raise forms.ValidationError(_('Veuillez renseigner ce champ'))
        if amount < 0:
            raise forms.ValidationError(_('Montant doit être supérieur à zéro'))
        return amount
    
    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        
  
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('name')
        if not nom:
                self.add_error('name', _('Veuillez renseigner ce champ .'))
        return cleaned_data