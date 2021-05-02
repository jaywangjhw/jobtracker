from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Position, Company, Account, Contact, Application
from .forms import PositionForm
import json


@login_required
def home(request):
    return render(request, 'jobs/home.html')

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
        # Pass the pk as a context variable, so that our templates can access it.
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


#-------------------------------------Position Views End------------------------------------------

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
        # Pass the pk as a context variable, so that our templates can access it.
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
        # Get the company query param from the request (may not be there).
        position_id = self.request.GET.get('position')
        # Check to see if the query param is there & make sure this is a 
        # GET request. We don't want to run this if the form is being POSTed.
        if position_id and self.request.method == "GET":
            # Grabs the initial dictionary by calling superclass.
            initial = super().get_initial()
            Position = Position.objects.get(pk=position_id)
            initial['position'] = position
            return initial
        # If this isn't a new Application for a specific position, just use the 
        # default initial values. 
        return super().get_initial()

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

class ContactListView(ListView):
    model = Contact
    template_name = 'jobs/contacts.html'
    context_object_name = 'contacts'


class ContactCreateView(CreateView):
    model = Contact
    context_object_name = 'contact'
    template_name = 'jobs/add_contact.html'
    fields = '__all__'
    success = '/contacts'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(UpdateView):
    model = Contact
    fields = '__all__'
    template_name = 'jobs/update_contact.html'
    context_object_name = 'contact'


class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy('jobs-contacts')


def account(request):
    account = Account.objects.all()
    
    context = {
        'title': 'Account',
        'account': account
    }
    return render(request, 'jobs/account.html', context)
