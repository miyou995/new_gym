from django.core.mail import send_mail
import logging
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ( UserCreationForm as DjangoUserCreationForm )
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from . import models 
from django.utils.translation import gettext_lazy as _


from django import forms

logger = logging.getLogger(__name__)
User = get_user_model()

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("email",'first_name', "last_name","groups", "is_staff", "is_active","picture","password1")
        field_classes = {"email": UsernameField}
        
  

class UserEditionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", 'first_name', "last_name",  "picture","is_active","is_staff",'is_admin',"groups")


class ChangePasswordForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = models.User
        fields = ('password',)
        widgets = {
            # 'first_name': forms.TextInput(attrs={'class' : 'form-control' }),
            'password'  : forms.PasswordInput(attrs={'class' : 'form-control' }),
        }
    # def __init__(self, ticket=None, *args, **kwargs):   
    #     super().__init__(*args, **kwargs)
    #     self.fields["password"].widget.attrs.update()

    #     self.fields['password'].error_messages = {
    #         'required': 'Veuillez renseigner ce champ.',
    #         'invalid': 'Custom error message for field1 is invalid.',
    #         # Add more custom error messages for different errors if needed
    #     }
    #     self.fields['password2'].error_messages = {
    #         'required': 'Veuillez renseigner ce champ.',
    #         'invalid': 'Custom error message for field1 is invalid.',
    #         # Add more custom error messages for different errors if needed
    #     }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2:
            if password != password2:
                self.add_error('password2', _("Les mots de passe ne correspondent pas."))
        return cleaned_data
    
  


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name','permissions', )




# --------------------------------------Authentication-------------------------------------------------
class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
            strip=False, widget=forms.PasswordInput 
    )
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password
            )
            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email/password combination."
            )
        logger.info(
            "Authentication successful for email=%s", email
            )
        return self.cleaned_data
    def get_user(self):
        return self.user 



class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = models.User
        fields = ('email' , 'password')
        widgets = {
            # 'first_name': forms.TextInput(attrs={'class' : 'form-control' }),
            'email'     : forms.EmailInput(attrs={'class' : 'form-control' }),
            'password'  : forms.PasswordInput(attrs={'class' : 'form-control' }),
        }




