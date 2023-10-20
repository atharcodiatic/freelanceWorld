from .models import *
from django import forms 
from accounts.models import *

class SkillRequiredField(forms.ModelMultipleChoiceField):
    
    def validate(self, value):
        return value
        

'''
skill_required = forms.ModelMultipleChoiceField(
        queryset = Skill.objects.filter(client=None), 
        widget  = forms.CheckboxSelectMultiple,
    )
'''

class JobPostForm(forms.ModelForm):
    skill_required = SkillRequiredField(
        queryset = Skill.objects.filter(client=None), 
        widget  = forms.CheckboxSelectMultiple,
    )

    class Meta:
        fields = '__all__'
        model = JobPost
        exclude= ['updated_at ', 'created_at', 'user', 'posted_at']



class SkillForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Skill
        exclude = ['client']
