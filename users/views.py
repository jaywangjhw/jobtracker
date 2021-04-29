from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import UserRegisterForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            username = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password')
            authenticate(username=username, password=pw)
            login(request, new_user)
            messages.success(request, f'Account created for {username}')
            return redirect('jobs-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
