from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return HttpResponse('<h1>Job Tracker Home</h1>')


def companies(request):
	return HttpResponse('<h1>Companies Page</h1>')
