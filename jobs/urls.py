from django.urls import path, include
from .views import *
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', CompanyListView.as_view(), name='jobs-companies'),
    path('companies/<int:pk>', CompanyDetailView.as_view(), name='jobs-company-details'),
    path('companies/edit/<int:pk>', CompanyUpdateView.as_view(), name='jobs-company-update'),
    path('companies/new', CompanyCreateView.as_view(extra_context={'title': 'Add Company'}), name='jobs-new-company'),
    path('companies/delete/<int:pk>', CompanyDeleteView.as_view(), name='jobs-company-delete'),
    path('positions/', PositionListView.as_view(), name='jobs-list-positions'),
    path('positions/new', PositionCreateView.as_view(), name='jobs-new-position'),
    path('positions/<int:pk>', PositionUpdateView.as_view(), name='jobs-update-position'),
    path('positions/delete/<int:pk>', PositionDeleteView.as_view(), name='jobs-delete-position'),
    path('applications/', ApplicationListView.as_view(), name='jobs-list-applications'),
    path('applications/new', ApplicationCreateView.as_view(), name='jobs-new-application'),
    path('applications/<int:pk>', ApplicationUpdateView.as_view(), name='jobs-update-application'),
    path('applications/delete/<int:pk>', ApplicationDeleteView.as_view(), name='jobs-delete-application'),
    path('account/', views.account, name='jobs-account'),
    path('contacts/', ContactListView.as_view(), name='jobs-contacts'),
    path('contacts/new', ContactCreateView.as_view(), name='jobs-new-contact'),
    path('contacts/<int:pk>', ContactUpdateView.as_view(), name='jobs-update-contact'),
    path('contacts/delete/<int:pk>', ContactDeleteView.as_view(), name='jobs-delete-contact'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete')
]

