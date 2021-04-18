from django import forms
from django.forms import ModelForm
from .models import Position, Company

# Need to add skills to db

class PositionForm(ModelForm):

    class Meta: 
        model = Position
        fields = '__all__'
        help_texts = {
            'date_opened': 'mm/dd/yyyy',
            'date_closed': 'mm/dd/yyyy'
        }


class NewCompanyForm(ModelForm):

	class Meta:
		model = Company
		fields = '__all__'
