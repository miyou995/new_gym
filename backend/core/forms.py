from django import forms

from django.utils.translation import gettext_lazy as _
from planning.models import Planning


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

