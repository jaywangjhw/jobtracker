from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
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


class CompanyListView(ListView):
    model = Company
    template_name = 'jobs/companies.html'
    context_object_name = 'companies'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    context_object_name = 'company'
    fields = ['name', 'careers_url', 'industry']
    success = '/companies'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = 'company'


class CompanyUpdateView(UpdateView):
    model = Company
    fields = '__all__'
    template_name_suffix = '_update_form'


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('jobs-companies')


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
