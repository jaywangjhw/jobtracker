from django.urls import path, include
from .views import *
from . import views
from users import views as user_views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', CompanyListView.as_view(extra_context={'title': 'Companies'}), name='jobs-companies'),
    path('companies/<int:pk>', CompanyDetailView.as_view(), name='jobs-company-detail'),
    path('companies/edit/<int:pk>', CompanyUpdateView.as_view(), name='jobs-company-update'),
    path('companies/new', CompanyCreateView.as_view(extra_context={'title': 'Add Company'}), name='jobs-new-company'),
    path('companies/delete/<int:pk>', CompanyDeleteView.as_view(), name='jobs-company-delete'),
    path('positions/', PositionListView.as_view(), name='jobs-list-positions'),
    path('positions/new', PositionCreateView.as_view(), name='jobs-new-position'),
    path('positions/<int:pk>', PositionUpdateView.as_view(), name='jobs-update-position'),
    path('positions/delete/<int:pk>', PositionDeleteView.as_view(), name='jobs-delete-position'),
    path('account/', views.account, name='jobs-account'),
    path('contacts/', ContactListView.as_view(), name='jobs-contacts'),
    path('contacts/new', ContactCreateView.as_view(), name='jobs-new-contact'),
    path('contacts/<int:pk>', ContactUpdateView.as_view(), name='jobs-update-contact'),
    path('contacts/delete/<int:pk>', ContactDeleteView.as_view(), name='jobs-delete-contact'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
]
