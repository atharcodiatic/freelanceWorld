from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
from django.forms import FileField ,ChoiceField
from django.core.validators import FileExtensionValidator
from .validators import validate_image
from django import forms
from cities_light.models import City
from django_countries.widgets import CountrySelectWidget
import datetime
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(country=self.instance.pk)
        
    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if len(data)<10:
            raise ValidationError("contact must be 10 digit")
    
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
                   'date_joined', 'is_active', 'is_staff', 'skills']
        
        
class FreelancerProfileUpdate(forms.ModelForm):
    ''' Form to update freelancer profile '''

    class Meta:
        model = Freelancer
        fields ='__all__'
        exclude = ["last_login", "is_superuser", 'groups', 'user_permissions',
                   'date_joined', 'is_active', 'is_staff', 'skills', 'password',
                    'username','password','confirm_password','country','city']
        
class ClientProfileUpdate(forms.ModelForm):
    ''' Form to update freelancer profile '''

    class Meta:
        model = Client
        fields ='__all__'
        exclude = ["last_login", "is_superuser", 'groups', 'user_permissions',
                   'date_joined', 'is_active', 'is_staff', 'password',
                    'username','password','confirm_password','country','city' ]
        

class SelfSkillForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = SelfSkills
        exclude = ['freelancer']

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

# def __init__(self, *args, **kwargs):
#         super(EntryForm, self).__init__(*args, **kwargs)
#         this_year = datetime.date.today().year
#         years = range(this_year-100, this_year+1)
#         years.reverse()

class EducationForm(forms.ModelForm):
    this_year = datetime.date.today().year
    years = range(this_year-100, this_year+8)
    start_date = forms.DateField(widget = forms.SelectDateWidget(years=years))
    end_date = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        fields = '__all__'
        model = Education
        exclude = ['freelancer']


class ClientProfile(forms.ModelForm):
    ''' Model Form For Client Profile'''

    confirm_password = password_fields()[1]
    password = password_fields()[0]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(country=self.instance.pk)
    
    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if len(data)<10:
            raise ValidationError("contact must be 10 digit")

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
    field_order = ['username', 'email', 'password', 'confirm_password']      
    class Meta:
        
        model = Client
        fields = '__all__'
        exclude = ["last_login", "is_superuser", 'groups', 'user_permissions',
                   'date_joined', 'is_active', 'is_staff',]
        
