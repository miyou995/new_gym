from django import forms
from django.utils.translation import gettext_lazy as _
from planning.models import Planning
from salle_activite.models import Salle ,Activity,Door
from client.models import Maladie
from abonnement.models import Abonnement


class PlanningModelForm(forms.ModelForm):
    
    class Meta:
        model  = Planning
        
        fields = ( 
             'name',
            'is_default',
             )
      

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update()

        self.fields['name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

class SalleModelForm(forms.ModelForm):
    
    class Meta:
        model  = Salle
        
        fields = ( 
             'name',
            'is_default',
             )

      
    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update()

        self.fields['name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

class MaladieModelForm(forms.ModelForm):
    
    class Meta:
        model  = Maladie

        fields = ( 
             'name',
             )
      

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update()

        self.fields['name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

class ActiviteModelForm(forms.ModelForm):
    
    class Meta:
        model  = Activity
        
        fields = ( 
             'name',
             'salle',
             'color',
             )
      

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update()

        self.fields['name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

class DoorModelForm(forms.ModelForm):
    
    class Meta:
        model  = Door
        
        fields = ( 
             'ip_adress',
            'salle',
            'username',
            'password'
             )
      

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["ip_adress"].widget.attrs.update()

        self.fields['ip_adress'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['salle'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['username'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

        self.fields['password'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }


class AbonnementModelForm(forms.ModelForm):
    
    class Meta:
        model  = Abonnement
        
        fields = ( 
            'type_of',
            'name',
            'price',
            'length',
            'seances_quantity',
            'salles',
             )
      

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
       

        self.fields['type_of'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }

        self.fields['name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['price'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['length'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['seances_quantity'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['salles'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
