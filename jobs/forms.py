from django import forms
from django.forms import ModelForm
from .models import Position, Company, Account, Contact, Application


class PositionForm(ModelForm):

    class Meta: 
        model = Position
        fields = ['company', 'position_title', 'position_url', 'date_opened', 'date_closed',
                    'skills', 'job_description']
        help_texts = {
            'position_url': "Ex: http://www.google.com",
            'date_opened': 'Ex: mm/dd/yyyy',
            'date_closed': 'Ex: mm/dd/yyyy'
        }


class AccountForm(ModelForm):

	class Meta:
		model = Account
		fields = '__all__'


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'careers_url', 'industry']


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        exclude = ('user',)


class CombinedApplicationForm(ApplicationForm):

    class Meta:
        model = Application
        exclude = ('user', 'company', 'position',)
        labels = {
            'email_used': 'What email address did you use to create this application?',
            'date_started': 'When did you start this application?',
            'date_submitted': 'If submitted, when?',
            'offer': 'Check if you\'ve received an offer',
            'accepted': 'Check if you\'ve accepted',
            'notes': 'Any notes specific to this application:'
        }


class CombinedPositionForm(PositionForm):

    class Meta:
        model = Position
        exclude = ('user', 'company', )
        labels = {
            'position_title': 'Job Title',
            'position_url': 'Job Posting URL',
            'date_opened': 'When did the job open?',
            'date_closed': 'When did the job close? (optional)'
        }


class CombinedCompanyForm(CompanyForm):

    class Meta:
        model = Company
        exclude = ('user',)
        labels = {
            'name': 'Company Name',
            'careers_url': 'Link to company careers page'
        }


