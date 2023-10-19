from .models import *
from django import forms 

class JobPostForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = JobPost

        