from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Position, Company, Account
from .forms import PositionForm
import json


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

# def add_position(request):

    # if request.method == 'POST':
    #     form = PositionForm(request.POST)

    #     # Render list of positions that have been added to db
    #     if form.is_valid():
    #         form.save()
    #         print("Redirecting to /positions")
    #         return redirect('/positions')

    # else:
    #     # Render blank Position form
    #     form = PositionForm()

    # context = {
    #     "form": form
    # }

    # return render(request, 'jobs/add_position.html', context)


# def update_position(request, pk):

    # position = Position.objects.get(id=pk)
    # form = PositionForm(instance=position)

    # if request.method == "POST":

    #     form = PositionForm(request.POST, instance=position)

    #     if form.is_valid():
    #         form.save()
    #         return redirect('/positions')

    # context = {
    #     'form': form
    # }

    # return render(request, 'jobs/update_position.html', context)


# def delete_position(request, pk):

    # position = Position.objects.get(id=pk) 
    # position.delete()   
    
    # return redirect('/positions')


# def list_positions(request):

    # list_positions = Position.objects.all()

    # context = {
    #     'title': 'Positions',
    #     'positions': list_positions,
    # }

    # return render(request, 'jobs/positions.html', context)


def account(request):
    account = Account.objects.all()
    
    context = {
        'title': 'Account',
        'account': account
    }
    return render(request, 'jobs/account.html', context)
