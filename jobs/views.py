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
from .models import Position, Company, Account, Contact, Communication, Application
from .forms import PositionForm, CompanyForm, ApplicationForm, CombinedPositionForm, CombinedApplicationForm, CombinedCompanyForm
from django.contrib import messages
from jobs.parse_url import get_domain_company, get_amazon_data
from jobs.reddit import get_reddit_data
import json



class HomeView(LoginRequiredMixin, View):

    def get(self, request):

        company_form = CombinedCompanyForm()
        position_form = CombinedPositionForm()
        application_form = CombinedApplicationForm()

        context = {'company_form': company_form}
        context['position_form'] = position_form
        context['application_form'] = application_form
        
        refresh = 0

        if request.GET.get('query') != None: 
            refresh = 1
            query = request.GET.get('query')
            subreddit = request.GET.get('subreddit')
            sort = request.GET.get('sort')
            limit = request.GET.get('results')

        else:
            query = "Software Engineer"
            subreddit = "software"
            sort = 'hot'
            limit = '5'

        results = get_reddit_data(limit, query, sort, subreddit)
        context['reddit_data'] = results

        positions = Position.objects.filter(user=request.user)
        
        positions_list = []

        for position in positions:
            positions_list.append(position.position_title)

        context['positions'] = positions_list

        if(refresh == 1):
            return JsonResponse(results, safe=False)

        return render(request, 'jobs/home.html', context)

    def post(self, request):
        context = {}
        # If there is a company_id in the form, then we know this company
        # already exists, and we do not want to re-save it
        if 'company_id' in request.POST:
            # Get the company instance so it can be used when creating the position/application
            company = Company.objects.get(pk=request.POST.get('company_id'))
        else:
            # If this is a new company, create a bounded form instance with the data from 
            # the post request. 
            company_form = CombinedCompanyForm(request.POST)
            company_form.instance.user = self.request.user

            if company_form.is_valid():
                company = company_form.save()
                messages.success(request, f'New Company Saved!')
            else:
                context['company_form']= company_form

        if 'position_id' in request.POST:
            position = Position.objects.get(pk=request.POST.get('position_id'))
        else:
            position_form = CombinedPositionForm(request.POST)
            position_form.instance.user = self.request.user
            position_form.instance.company = company

            if position_form.is_valid():
                position = position_form.save()
                messages.success(request, f'New Position Saved!')
            else:
                context['position_form'] = position_form

        application_form = CombinedApplicationForm(request.POST)
        application_form.instance.user = self.request.user
        application_form.instance.company = company
        application_form.instance.position = position

        if application_form.is_valid():
            application = application_form.save()
            messages.success(request, f'New Application Saved!')
            return redirect('jobs-home')
        else:
            context['application_form'] = application_form

        return render(request, 'jobs/home.html', context) 


@login_required
@ensure_csrf_cookie
def parse_job_url(request):
    job_data = {}
    # Job posting url should be passed in as a query parram
    url = request.GET.get('app-url')
    
    # See if this user already tracks this specific position
    if Position.objects.filter(user=request.user, position_url=url).exists():
        position = Position.objects.filter(user=request.user, position_url=url).first()
        job_data['position_message'] = 'This application is for a position you already track!'
        job_data['company_id'] = position.company.id
        job_data['company'] = position.company.name
        job_data['position_id'] = position.id
        job_data['position_title'] = position.position_title
    else:
        # If this is a new position, we need to parse the url to get any relevant data
        job_data = get_amazon_data(url)

        if job_data:
            if 'company' in job_data:
                # Check if the user already tracks this company
                company = Company.objects.filter(name__icontains=job_data['company'], user=request.user).first()
                if company:
                    job_data['company_id'] = company.id
                    job_data['company'] = company.name
                    job_data['company_message'] = 'This application is for a company you already track!'
                else:
                    # Need to add more fields from the parsed data here...
                    job_data['company_message'] = 'You are not tracking this company yet. So we\'ll add it to your companies list!'
        else:
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


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    context_object_name = 'position'
    template_name = 'jobs/add_position.html'
    fields = ['company', 'position_title', 'position_url', 'date_opened', 'date_closed',
                'skills', 'job_description']
    success = '/positions'

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
    context_object_name = 'application'
    template_name = 'jobs/add_application.html'
    fields = ['position', 'date_started', 'date_submitted', 'email_used', 'offer',
                'accepted', 'notes']
    success = '/applications'

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


#-------------------------------------Applications Views End------------------------------------------

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'jobs/contacts.html'
    context_object_name = 'contacts'


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


class CommunicationCreateView(LoginRequiredMixin, CreateView):
    
    model = Communication
    template_name = 'jobs/add_communication.html'
    context_object_name = 'comms'
    fields = ['application', 'contact', 'date', 'method', 'notes']
    success_url = reverse_lazy('jobs-list-communications')

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

@login_required
def account(request):
    account = Account.objects.all()
    
    context = {
        'title': 'Account',
        'account': account
    }
    return render(request, 'jobs/account.html', context)

