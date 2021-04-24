from django.urls import path
from .views import CompanyListView, CompanyCreateView, CompanyDetailView
from . import views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', CompanyListView.as_view(), name='jobs-companies'),
    path('companies/<int:pk>', CompanyDetailView.as_view(), name='jobs-company-detail'),
    path('companies/new', CompanyCreateView.as_view(), name='jobs-new-company'),
    path('positions/', views.list_positions, name='jobs-positions'),
    path('positions/new', views.add_position, name='jobs-new-position'),
    path('account/', views.account, name='jobs-account'),
]
