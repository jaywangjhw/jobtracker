from django.shortcuts import render
from django.http import HttpResponse
from .models import Position


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

def positions(request):

	list_positions = Position.objects.all()

	context = {
		'title': 'Positions',
		'positions': list_positions,
	}

	return render(request, 'jobs/positions.html', context)