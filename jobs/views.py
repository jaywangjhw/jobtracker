from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Position, Company
from .forms import PositionForm, NewCompanyForm
import json


def home(request):
    return render(request, 'jobs/home.html')


def companies(request):
    all_companies = Company.objects.all()
    
    context = {
        'title': 'Companies',
        'companies': all_companies
    }
    return render(request, 'jobs/companies.html', context)


def add_company(request):
	if request.method == 'POST':
		form = NewCompanyForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/companies')
	else:
		form = NewCompanyForm()

	context = {
		'form': form,
	}
	return render(request, 'jobs/add_company.html', context)


def add_position(request):

    if request.method == 'POST':
        form = PositionForm(request.POST)

        # Render list of positions that have been added to db
        if form.is_valid():
            print("Saving Position data")
            form.save()
            print("Redirecting to /positions")
            return HttpResponseRedirect('/positions')

    else:
        # Render blank Position form
        form = PositionForm()

    context = {
        "form": form
    }

    print("Rendering add_position.html")
    return render(request, 'jobs/add_position.html', context)


def list_positions(request):

    list_positions = Position.objects.all()

    context = {
        'title': 'Positions',
        'positions': list_positions,
    }

    return render(request, 'jobs/positions.html', context)
