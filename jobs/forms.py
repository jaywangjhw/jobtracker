from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple
from .models import (Position, 
                     Company,
                     Account, 
                     Contact, 
                     Application, 
                     Communication, 
                     Interview, 
                     Assessment, 
                     Skill)
from users.models import Document


class PositionForm(ModelForm):

    class Meta: 
        model = Position
        fields = ['company', 'position_title', 'position_url', 'date_opened', 'date_closed',
                    'skills', 'job_description']
        help_texts = {
            'date_opened': 'Ex: mm/dd/yyyy or yyyy-mm-dd',
            'date_closed': 'Ex: mm/dd/yyyy or yyyy-mm-dd'
        }
        labels = {
            'position_title': 'Job Title',
            'position_url': 'Job Posting URL',
            'date_opened': 'When did the job open?',
            'date_closed': 'When did the job close? (optional)'
        }

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the company dropdown field to only those companies
            this user has added. Same thing for the list of Skills to chose from. 
        '''
        user = kwargs.pop('user')
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(user=user)
        self.fields['skills'].queryset = Skill.objects.filter(user=user)


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
        labels = {
            'email_used': 'What email address did you use to create this application?',
            'date_started': 'When did you start this application?',
            'date_submitted': 'If submitted, when?',
            'offer': 'Check if you\'ve received an offer',
            'accepted': 'Check if you\'ve accepted',
            'notes': 'Any notes specific to this application:'
        }

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the position dropdown field to only those positions
            this user has added.
        '''
        user = kwargs.pop('user')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['position'].queryset = Position.objects.filter(user=user)
        self.fields['resume'].queryset = Document.objects.filter(user=user)


class CommunicationForm(ModelForm):

    class Meta: 
        model = Communication
        fields = ['application', 'contact', 'date', 'method', 'notes']
        help_texts = {
            'date': 'Ex: mm/dd/yyyy',
        }

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the company dropdown field to only those companies
            this user has added.
        '''
        user = kwargs.pop('user')
        super(CommunicationForm, self).__init__(*args, **kwargs)
        self.fields['application'].queryset = Application.objects.filter(user=user)
        self.fields['contact'].queryset = Contact.objects.filter(user=user)


class InterviewForm(ModelForm):

    class Meta:
        model = Interview
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the application dropdown field to only the application
            from which the user selected to create a new interview
        '''
        pk = kwargs.pop('app_pk')
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields['application'].queryset = Application.objects.filter(pk=pk)
        self.fields['date'].required = True


class AssessmentForm(ModelForm):

    class Meta:
        model = Assessment
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the application dropdown field to only the application
            from which the user selected to create a new assessment
        '''
        pk = kwargs.pop('app_pk')
        super(AssessmentForm, self).__init__(*args, **kwargs)
        self.fields['application'].queryset = Application.objects.filter(pk=pk)
        self.fields['date'].required = True


class CombinedApplicationForm(ModelForm):

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
    
    def __init__(self, *args, **kwargs):
        ''' This filters the options in the position dropdown field to only those positions
            this user has added.
        '''
        user = kwargs.pop('user')
        super(CombinedApplicationForm, self).__init__(*args, **kwargs)
        self.fields['resume'].queryset = Document.objects.filter(user=user)


class CombinedPositionForm(ModelForm):

    class Meta:
        model = Position
        exclude = ('user', 'company', )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        ''' This filters the options in the skills selection field to only those skills
            this user has added.
        '''
        user = kwargs.pop('user')
        super(CombinedPositionForm, self).__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.filter(user=user)


class CombinedCompanyForm(CompanyForm):

    class Meta:
        model = Company
        exclude = ('user',)
        labels = {
            'name': 'Company Name',
            'careers_url': 'Link to company careers page'
        }
