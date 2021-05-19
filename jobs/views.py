from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Position, Company, Account, Contact, Communication, Application, Interview, Assessment
from .forms import (ApplicationForm,
                    CombinedPositionForm,
                    CombinedApplicationForm,
                    CombinedCompanyForm,
                    CommunicationForm,
                    CompanyForm,
                    PositionForm)
from django.contrib import messages
from jobs.parse_url import get_job_data
import json



class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        company_form = CombinedCompanyForm()
        combined_position_form = CombinedPositionForm()
        full_position_form = PositionForm(user=request.user)
        combined_application_form = CombinedApplicationForm()
        full_application_form = ApplicationForm(user=request.user)

        context = {'company_form': company_form}
        context['combined_position_form'] = combined_position_form
        context['full_position_form'] = full_position_form
        context['combined_application_form'] = combined_application_form
        context['full_application_form'] = full_application_form

        applications = Application.objects.filter(user=self.request.user).values()

        for app in applications:
            position = Position.objects.get(pk=app['position_id'])
            app['position'] = position.position_title
            app['company'] = position.company.name

            if app['accepted'] and app['accepted'] == True:
                status = "Accepted"
            elif app['offer'] and app['offer'] == True:
                status = 'Received Offer'
            elif Interview.objects.filter(application=app['id']):
                status = 'Interviewed'
            elif app['date_submitted']:
                status = 'Submitted'
            else:
                status = 'Started'

            app['status'] = status

        context['applications'] = applications

        return render(request, 'jobs/home.html', context)


    def post(self, request):
        context = {}
        # If position is in the form, then we know this is solely an application form
        # which will be for an existing position.
        if 'position' in request.POST:
            application_form = ApplicationForm(request.POST, user=self.request.user)
            application_form.instance.user = self.request.user
            
            if application_form.is_valid():
                application = application_form.save()
                messages.success(request, f'New Application Saved!')
            else:
                context['application_form'] = application_form
        else:
            # Otherwise, this is a new position and new application for an existing company
            # or it's a new company, new position, and new application. 
            company = None
            position = None
            
            # If company is in the form, this is a position for an existing company.
            if 'company' in request.POST:
                position_form = PositionForm(request.POST, user=self.request.user)
            else:
                position_form = CombinedPositionForm(request.POST)

                company_form = CombinedCompanyForm(request.POST)
                company_form.instance.user = self.request.user

                if company_form.is_valid():
                    company = company_form.save()
                    messages.success(request, f'New Company Saved!')
                else:
                    context['company_form'] = company_form

            position_form.instance.user = self.request.user
            if company:
                position_form.instance.company = company

            if position_form.is_valid():
                position = position_form.save()
                messages.success(request, f'New Position Saved!')
            else:
                context['position_form'] = position_form

            application_form = CombinedApplicationForm(request.POST)
            application_form.instance.user = self.request.user
            if position:
                application_form.instance.position = position
            
            if application_form.is_valid():
                application = application_form.save()
                messages.success(request, f'New Application Saved!')
                return redirect('jobs-home')
            else:
                context['application_form'] = application_form

        return redirect(reverse_lazy('jobs-home'))


@login_required
@ensure_csrf_cookie
def parse_job_url(request):
    job_data = {}
    print(request)
    # Job posting url should be passed in as a query param
    if 'app_url' in request.GET:
        url = request.GET.get('app_url')
    else:
        return JsonResponse(job_data)

    # Company ID may/may not be passed as a param
    if 'company_id' in request.GET:
        company_name = Company.objects.get(pk=request.GET.get('company_id')).name
    else:
        company_name = None
    
    print(url)
    # ** NEED TO EXPAND ** Right now only set up for amazon urls.
    job_data = get_job_data(url, company_name)

    if not job_data:
        job_data['company_message'] = 'We couldn\'t figure out many details from this url. Please fill out the form manually.'
 
    return JsonResponse(job_data)


#-------------------------------------Company Views----------------------------------------
class CompanyListView(LoginRequiredMixin, View):
    
    def get(self, request):
        # If it's there, grab the company's pk from the request query param
        comp_id = request.GET.get('company')

        # Check if this was called via AJAX
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            company = Company.objects.get(pk=comp_id)
            response = {
                'name': company.name, 
                'careers_url': company.careers_url, 
                'industry': company.industry,
                'id': company.id
            }
            return JsonResponse(response)
        else:
            companies = Company.objects.filter(user=request.user)
            context = {'companies': companies}
            
            if comp_id:
                show_co = Company.objects.get(pk=comp_id)
                context['show_co'] = show_co

            return render(request, 'jobs/companies.html', context)


class CompanyCreateView(LoginRequiredMixin, CreateView):
    
    model = Company
    context_object_name = 'company'
    fields = ['name', 'careers_url', 'industry']
    success_url = reverse_lazy('jobs-companies')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Company
    fields = ['name', 'careers_url', 'industry']
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the PK from the url so that we can set a 'back' button that will go back
        # showing this company's details on the Companies page.
        context['id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Add query params so the updated company's details will be displayed, when
        # routing back to the Companies page.
        return reverse_lazy('jobs-companies') + "?company=" + str(self.kwargs['pk'])


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Company
    success_url = reverse_lazy('jobs-companies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the pk as a context variable, so that our templtes can access it.
        context['id'] = self.kwargs['pk']
        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):

    model = Company
    template_name = 'jobs/company_detail.html'
    context_object_name = 'company'


#-------------------------------------Company Views End----------------------------------------

#---------------------------------------Position Views-----------------------------------------

class PositionListView(LoginRequiredMixin, ListView):
    
    model = Position
    template_name = 'jobs/positions.html'
    context_object_name = 'positions'
    fields = ['company', 'position_title', 'position_url', 'date_opened', 'date_closed',
                'skills', 'job_description']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm
    context_object_name = 'position'
    template_name = 'jobs/add_position.html'
    success = '/positions'

    def get_form_kwargs(self):
        ''' Allows us to pass in the user to the kwargs when the form is created. Then, within
            the PositionForm class, the __init__ filters the company queryset to only those
            companies for this user.
        '''
        kwargs = super(PositionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        ''' Allows you to set initial values for the new Position form. 
            Currently set up to receive a URL query param with a Company's PK. 
            This will then set the initial form value for the Company. 
        '''
        # Get the company query param from the request (may not be there).
        company_id = self.request.GET.get('company')
        # Check to see if the query param is there & make sure this is a 
        # GET request. We don't want to run this if the form is being POSTed.
        if company_id and self.request.method == "GET":
            # Grabs the initial dictionary by calling superclass.
            initial = super().get_initial()
            company = Company.objects.get(pk=company_id)
            initial['company'] = company
            return initial
        # If this isn't a new Position for a specific company, just use the 
        # default initial values. 
        return super().get_initial()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = ['company', 'position_title', 'position_url', 'date_opened', 'date_closed',
                'skills', 'job_description']
    template_name = 'jobs/update_position.html'
    context_object_name = 'position'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('jobs-list-positions')


#-------------------------------------Position Views End----------------------------------------

#---------------------------------------Application Views-----------------------------------------

class ApplicationListView(LoginRequiredMixin, ListView):
    
    model = Application
    template_name = 'jobs/applications.html'
    context_object_name = 'applications'
    fields = ['position', 'date_started', 'date_submitted', 'email_used', 'offer',
                'accepted', 'notes']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):

        offer = Application.objects.all().filter(offer=True).count()
        accepted = Application.objects.all().filter(accepted=True).count()

        context = super().get_context_data(**kwargs)
        # Pass the offer_count and accepted_count as context variables, so that our templates can access.
        context['offer_count'] = offer
        context['accepted_count'] = accepted
        return context


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    context_object_name = 'application'
    template_name = 'jobs/add_application.html'
    success = '/applications'

    def get_form_kwargs(self):
        ''' Allows us to pass in the user to the kwargs when the form is created. Then, within
            the ApplicationForm class, the __init__ filters the position queryset to only those
            positions for this user.
        '''
        kwargs = super(ApplicationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        ''' Allows you to set initial values for the new Application form. 
            Currently set up to receive a URL query param with a Position PK. 
            This will then set the initial form value for the Position. 
        '''
        # Grabs the initial dictionary by calling superclass.
        initial = super().get_initial()
        # Get the position query param from the request (may not be there).
        position_id = self.request.GET.get('position')
        # Check to see if the query param is there & make sure this is a 
        # GET request. We don't want to run this if the form is being POSTed.
        if self.request.method == "GET" and position_id:
            position = Position.objects.get(pk=position_id)
            initial['position'] = position

        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Application
    fields = ['position', 'date_started', 'date_submitted', 'email_used', 'offer',
                'accepted', 'notes']
    template_name = 'jobs/update_application.html'
    context_object_name = 'application'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('jobs-list-applications')


class ApplicationDetailView(LoginRequiredMixin, DetailView):

    model = Application
    template_name = 'jobs/application_detail.html'
    context_object_name = 'app'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interviews'] = Interview.objects.filter(application=self.kwargs['pk'])
        context['assessments'] = Assessment.objects.filter(application=self.kwargs['pk'])
        context['communications'] = Communication.objects.filter(application=self.kwargs['pk'], user=self.request.user)
        print(context)
        return context



#-------------------------------------Applications Views End------------------------------------------

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'jobs/contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    context_object_name = 'contact'
    template_name = 'jobs/add_contact.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'notes']
    success = '/contacts'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = '__all__'
    template_name = 'jobs/update_contact.html'
    context_object_name = 'contact'


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('jobs-contacts')

#-------------------------------------Communication Views----------------------------------------

class CommunicationListView(LoginRequiredMixin, ListView):
    
    model = Communication
    template_name = 'jobs/communications.html'
    context_object_name = 'comms'
    fields = ['application', 'contact', 'date', 'method', 'notes']
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CommunicationCreateView(LoginRequiredMixin, CreateView):
    
    model = Communication
    form_class = CommunicationForm
    template_name = 'jobs/add_communication.html'
    context_object_name = 'comms'
    success_url = reverse_lazy('jobs-list-communications')

    def get_form_kwargs(self):
        ''' Allows us to pass in the user to the kwargs when the form is created. Then, within
            the CommunicationForm class, the __init__ filters the application and contact querysets
            to only those added by this user.
        '''
        kwargs = super(CommunicationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        ''' Allows you to set initial values for the new Communication form. 
            Currently set up to receive URL query params with either a Contact PK,
            or an Application PK. 
            This will then set the initial form value for either. 
        '''
        # Grab the initial dictionary by calling superclass.
        initial = super().get_initial()

        # GET request. We don't want to run this if the form is being POSTed.
        if self.request.method == "GET":
            # Get the Application query param from the request (may not be there).
            app_id = self.request.GET.get('application')
            # Get the Contact query param from the request (may not be there).
            contact_id = self.request.GET.get('contact')

            if app_id:
                application = Application.objects.get(pk=app_id)
                initial['application'] = application
            elif contact_id:
                contact = Contact.objects.get(pk=contact_id)
                initial['contact'] = contact
            
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommunicationUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Communication
    fields = ['application', 'contact', 'date', 'method', 'notes']
    template_name = 'jobs/update_communication.html'
    context_object_name = 'comms'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommunicationDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Communication
    success_url = reverse_lazy('jobs-list-communications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the pk as a context variable, so that our templtes can access it.
        context['id'] = self.kwargs['pk']
        return context


#-------------------------------------Communication Views End-------------------------------------


#-------------------------------------Interview Views----------------------------------------
class InterviewListView(LoginRequiredMixin, ListView):
    model = Interview
    template_name = 'jobs/interviews.html'
    context_object_name = 'comms'
    fields = ['application', 'date', 'time', 'location', 'virtual_url', 'complete', 'notes']
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

#-------------------------------------Interview Views End-------------------------------------

@login_required
def account(request):
    account = Account.objects.all()
    
    context = {
        'title': 'Account',
        'account': account
    }
    return render(request, 'jobs/account.html', context)

