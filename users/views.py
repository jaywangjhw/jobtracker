from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Document


def register(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            username = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password')
            authenticate(username=username, password=pw)
            login(request, new_user, backend=backend)
            messages.success(request, f'Account created for {username}')
            return redirect('jobs-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/profile.html', context)


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['upload' ]
    success_url = reverse_lazy('upload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        documents = Document.objects.filter(user=self.request.user)
        
        context['documents'] = documents
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
