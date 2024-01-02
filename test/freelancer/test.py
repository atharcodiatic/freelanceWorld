from django.test import TestCase
from jobs.forms import JobProposalForm
from django.core.validators import FileExtensionValidator
from django.core import validators

class JobProposalFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = JobProposalForm()
        self.assertTrue(form.fields['resume'].label is not None or form.fields['resume'].label == 'resume')

    def test_renew_form_date_field_help_text(self):
        form = JobProposalForm()
        field_valdtr = form.fields['resume'].validators
        self.assertFalse(any(isinstance(validator,FileExtensionValidator) for validator in field_valdtr))

    def test_other_currency(self):
        form = JobProposalForm(data={'currency': 'INDIA'})
        self.assertFalse(form.is_valid())

