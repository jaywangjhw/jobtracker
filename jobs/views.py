from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Position
from .forms import PositionForm
import json

def home(request):
	return render(request, 'jobs/home.html')

def companies(request):
	# placeholder data to render the template with content.
	# This will be replaced with actual data from models.py
	companies = [
		{
			'name': 'Amazon',
			'careers_url': 'www.amazon.com/careers',
			'industry': 'Tech'
		}, 
		{
			'name': 'Flatiron',
			'careers_url': 'www.flatiron.com/careers',
			'industry': 'Healthcare'
		}, 
		{
			'name': 'Google',
			'careers_url': 'www.google.com/careers',
			'industry': 'Tech'
		}
	]

	context = {
		'title': 'Companies',
		'companies': companies
	}

	return render(request, 'jobs/companies.html', context)

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