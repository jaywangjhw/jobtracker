from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return render(request, 'jobs/home.html')


def companies(request):
	return render(request, 'jobs/companies.html')
