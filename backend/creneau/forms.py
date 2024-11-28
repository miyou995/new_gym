from django import forms
from .models import Creneau



class CreneauModelForm(forms.ModelForm):
    class Meta :
        model = Creneau 
        fields =(
            'name',
            'activity',
            'coach',
            'planning',
            'day',
            'hour_start',
            'hour_finish',
            'color',
        )
        widgets = {
            'hour_start': forms.TimeInput(attrs={'type': 'time'}),
            'hour_finish': forms.TimeInput(attrs={'type': 'time'}),
            'color': forms.TextInput(attrs={'type': 'color'}),


        }

    def __init__(self, ticket=None, *args, **kwargs):   
        super().__init__(*args, **kwargs)

        self.fields['activity'].error_messages = {
            'required': 'veuillez choisir.',
            'invalid': 'Custom error message for field1 is invalid.',
          
        }
        self.fields['planning'].error_message ={
            'required':'veuillez choisir',
            'invalid': 'Custom error message for field1 is invalid.',
        }
        self.fields['day'].error_message ={
            'required':'veuillez choisir',
            'invalid': 'Custom error message for field1 is invalid.',
        }
        self.fields['hour_start'].error_message ={
            'required':'veuillez choisir',
            'invalid': 'Custom error message for field1 is invalid.',
        }
        self.fields['hour_finish'].error_message ={
            'required':'veuillez choisir',
            'invalid': 'Custom error message for field1 is invalid.',
        }
        
