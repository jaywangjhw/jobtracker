from django import forms
from django.forms import ModelForm
from .models import Position, Company, Account, Contact


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