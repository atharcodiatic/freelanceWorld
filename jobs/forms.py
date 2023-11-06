from .models import *
from django import forms 
from accounts.models import *

class SkillRequiredField(forms.ModelMultipleChoiceField):
    def validate(self, value):
        return value
    

    def _check_values(self, value):
        """
        Given a list of possible PK values, return a QuerySet of the
        corresponding objects. Raise a ValidationError if a given value is
        invalid (not a valid PK, not in the queryset, etc.)
        """
        key = self.to_field_name or "pk"
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages["invalid_list"],
                code="invalid_list",
            )
        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
            except (ValueError, TypeError):
                raise ValidationError(
                    self.error_messages["invalid_pk_value"],
                    code="invalid_pk_value",
                    params={"pk": pk},
                )
        qs = self.queryset.filter(**{"%s__in" % key: value})
        pks = {str(getattr(o, key)) for o in qs}
        
    
        return qs
    
    def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        value = self.to_python(value)
        self.validate(value)
        
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

    def clean_skill_required(self):
        data = self.cleaned_data["skill_required"]
        return data

    class Meta:
        fields = '__all__'
        model = JobPost
        exclude= ['updated_at ', 'created_at', 'user', 'posted_at']



class SkillForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Skill
        exclude = ['client']


class JobProposalForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = JobProposal
        exclude = ['updated_at ', 'created_at', 'user', 'job','status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_message']
