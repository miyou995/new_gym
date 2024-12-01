from django import forms
from .models import Client,Coach,Personnel,Maladie
from django.utils.translation import gettext_lazy as _
import re


class ClientModelForm(forms.ModelForm):
    carte = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Veuillez entrer un numéro de carte valide.',
        }
    )
    maladies = forms.ModelMultipleChoiceField(
        queryset=Maladie.objects.all(),
        required=False,
    )
    class Meta:
        model  = Client
        
        fields = ( 
        "carte",
        "last_name",
        "first_name",
        "picture",
        "email",
        "adress",
        "phone",
        "civility",
        "nationality",
        "birth_date",
        "blood",
        'maladies',
        'note')
        widgets = {
           
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs.update()

        self.fields['last_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
            # Add more custom error messages for different errors if needed
        }
        self.fields['first_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['blood'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }


    def clean(self):
        cleaned_data = super().clean()
        card=cleaned_data.get('carte')
        phone=cleaned_data.get('phone')
        last_name=cleaned_data.get('last_name')

        if not last_name :
            self.add_error('last_name',_("Veuillez renseigner ce champ "))
     
        if not phone :
            self.add_error('phone',_("Veuillez renseigner ce champ "))
        
        if phone:
            trim_phone = phone.replace(" ", "")
            phone_pattern = re.compile(r'^(0)(5|6|7)[0-9]{8}$')
            if not phone_pattern.match(trim_phone):
                self.add_error('phone', _("Veuillez entrer un numéro de téléphone valide "))  
        return cleaned_data
    
    
class CoachModelForm(forms.ModelForm):
    
    class Meta:
        model  = Coach
        
        fields = ( 
        "last_name",
        "first_name",
        "email",
        "adress",
        "birth_date",
        "nationality",
        "phone",
        "civility",
        "blood",
        'color',
        'pay_per_hour',
        'note')
        widgets = {
           
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs.update()

        self.fields['last_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
            # Add more custom error messages for different errors if needed
        }
        self.fields['first_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['birth_date'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['blood'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['nationality'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field2 is invalid.',
        }

    def clean(self):
        cleaned_data = super().clean()
        phone=cleaned_data.get('phone')
   
      
        if not phone :
            self.add_error('phone',_("Veuillez renseigner ce champ "))
        if phone:
            phone_pattern = re.compile(r'^(0)(5|6|7)[0-9]{8}$')
            if not phone_pattern.match(phone):
                self.add_error('phone',_("Veuillez entrer un numéro de téléphone valide "))  
        return cleaned_data
   


class PersonnelModelForm(forms.ModelForm):
    
    class Meta:
        model  = Personnel
        
        fields = ( 
        "last_name",
        "first_name",
        "function",
        "adress",
        "birth_date",
        "nationality",
        "phone",
        "civility",
        "blood",
        "state",
        'note')

        widgets = {
           
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs.update()

        self.fields['last_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field1 is invalid.',
            # Add more custom error messages for different errors if needed
        }
        self.fields['first_name'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['birth_date'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['blood'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field2 is invalid.',
        }
        self.fields['nationality'].error_messages = {
            'required': 'Veuillez renseigner ce champ.',
            'invalid': 'Custom error message for field2 is invalid.',
        }

    def clean(self):
        cleaned_data = super().clean()
        phone=cleaned_data.get('phone')
  
        if not phone :
            self.add_error('phone',_("Veuillez renseigner ce champ "))
        if phone:
            phone_pattern = re.compile(r'^(0)(5|6|7)[0-9]{8}$')
            if not phone_pattern.match(phone):
                self.add_error('phone',_("Veuillez entrer un numéro de téléphone valide "))  
        return cleaned_data
   
