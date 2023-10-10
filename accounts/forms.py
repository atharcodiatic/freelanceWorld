from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
from django.forms import FileField ,ChoiceField
from django.core.validators import FileExtensionValidator
from .validators import validate_image
from django import forms

class CustomUserCreationForm(UserCreationForm): 

    ''' Used in admin panel to create user instance'''
    profile_pic = FileField(
                    validators=[validate_image,
                    FileExtensionValidator(
                            allowed_extensions=["png",'jpeg'],
                            message='only jpeg and png extensions allowed')])

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",) 

# class RegistrationForm(CustomUserCreationForm):

#     ''' rendered on user registration view '''

#     CHOICES =( 
#     ("FR", "Freelancer"), 
#     ("CL", "Client"), ) 

#     user_type = forms.ChoiceField(choices =CHOICES, 
#                       widget = forms.Select(attrs = {'onchange' : "myFunction(this.value);"}))
    
#     class Meta(CustomUserCreationForm.Meta):
#         fields = '__all__' 
#         exclude = ["last_login","is_superuser",'groups','user_permissions',
#                    'date_joined','is_active','is_staff','password']
        

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)

    attrs = {
        "type": "password"
    }
    password = forms.CharField(widget=forms.TextInput(attrs=attrs))

def password_fields():

    ''' 
    this function returns the  custom password fields for Profile Forms
    '''

    attrs = {
        "type": "password"
    }

    confirm_password = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    password = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
    
    return [password, confirm_password, ]

class FreelancerProfile(forms.ModelForm):
    confirm_password = password_fields()[1]
    password = password_fields()[0]

    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password and password :
            if password != confirm_password:
                raise ValidationError(
                    "password does not match."
                )

    
    
    class Meta:
        model = Freelancer
        fields = '__all__'

        exclude = ["last_login", "is_superuser", 'groups', 'user_permissions',
                   'date_joined', 'is_active', 'is_staff','skills']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['created_at',]


        
class ClientProfile(forms.ModelForm):

    ''' Model Form For Client Profile'''

    confirm_password = password_fields()[1]
    password = password_fields()[0]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password and password :
            # Only do something if both fields are valid so far.
            if password != confirm_password:
                raise ValidationError(
                    "password does not match."
                )

    class Meta:
        
        model = Client
        fields = '__all__'
        field_order = ['username', 'email', 'password', 'confirm_password']
        exclude = ["last_login", "is_superuser", 'groups', 'user_permissions',
                   'date_joined', 'is_active', 'is_staff',]