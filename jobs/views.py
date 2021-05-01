from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Position, Company, Account, Contact
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
        # Pass the pk as a context variable, so that our templtes can access it.
        context['id'] = self.kwargs['pk']
        return context

#-------------------------------------Company Views End----------------------------------------

class PositionListView(ListView):
    
    model = Position
    template_name = 'jobs/positions.html'
    context_object_name = 'positions'


class PositionCreateView(CreateView):
    model = Position
    context_object_name = 'position'
    template_name = 'jobs/add_position.html'
    fields = '__all__'
    success = '/positions'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PositionUpdateView(UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'jobs/update_position.html'
    context_object_name = 'position'


class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('jobs-list-positions')


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
